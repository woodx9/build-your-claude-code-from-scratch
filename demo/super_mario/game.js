class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        this.gameState = 'start';
        this.score = 0;
        this.lives = 3;
        this.coins = 0;
        
        this.camera = { x: 0, y: 0 };
        this.gravity = 0.8;
        this.friction = 0.8;
        
        this.keys = {};
        this.mario = null;
        this.platforms = [];
        this.enemies = [];
        this.collectibles = [];
        this.particles = [];
        
        this.soundManager = new SoundManager();
        this.levelWidth = 3200;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.createLevel();
        this.mario = new Mario(100, 400, this);
        this.gameLoop();
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            if (e.code === 'Space') e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
        
        document.getElementById('startBtn').addEventListener('click', () => {
            this.startGame();
        });
        
        document.getElementById('restartBtn').addEventListener('click', () => {
            this.restartGame();
        });
    }
    
    createLevel() {
        this.platforms = [
            new Platform(0, 550, 800, 50, this),
            new Platform(900, 550, 400, 50, this),
            new Platform(1400, 450, 200, 20, this),
            new Platform(1700, 350, 200, 20, this),
            new Platform(2000, 450, 300, 20, this),
            new Platform(2400, 350, 200, 20, this),
            new Platform(2700, 550, 500, 50, this),
            
            new Platform(200, 400, 100, 20, this),
            new Platform(450, 350, 100, 20, this),
            new Platform(650, 300, 100, 20, this),
            new Platform(1100, 400, 150, 20, this),
        ];
        
        this.enemies = [
            new Goomba(300, 520, this),
            new Goomba(600, 520, this),
            new Goomba(1000, 520, this),
            new Goomba(1500, 420, this),
            new Goomba(2100, 420, this),
            new Goomba(2800, 520, this),
        ];
        
        this.collectibles = [
            new Coin(250, 350, this),
            new Coin(500, 300, this),
            new Coin(700, 250, this),
            new Coin(1150, 350, this),
            new Coin(1450, 400, this),
            new Coin(1750, 300, this),
            new Coin(2050, 400, this),
            new Coin(2450, 300, this),
            new PowerUp(400, 300, this),
            new PowerUp(1600, 300, this),
        ];
    }
    
    startGame() {
        this.gameState = 'playing';
        document.getElementById('startScreen').classList.add('hidden');
    }
    
    restartGame() {
        this.gameState = 'playing';
        this.score = 0;
        this.lives = 3;
        this.coins = 0;
        this.camera.x = 0;
        this.mario = new Mario(100, 400, this);
        this.createLevel();
        this.particles = [];
        document.getElementById('gameOver').classList.add('hidden');
        this.updateUI();
    }
    
    gameLoop() {
        this.update();
        this.render();
        requestAnimationFrame(() => this.gameLoop());
    }
    
    update() {
        if (this.gameState !== 'playing') return;
        
        this.mario.update();
        
        this.enemies.forEach(enemy => enemy.update());
        this.enemies = this.enemies.filter(enemy => !enemy.destroyed);
        
        this.collectibles.forEach(item => item.update());
        this.collectibles = this.collectibles.filter(item => !item.collected);
        
        this.particles.forEach(particle => particle.update());
        this.particles = this.particles.filter(particle => particle.life > 0);
        
        this.updateCamera();
        
        if (this.mario.y > this.height) {
            this.loseLife();
        }
        
        if (this.mario.x > this.levelWidth - 100) {
            this.winLevel();
        }
    }
    
    updateCamera() {
        this.camera.x = this.mario.x - this.width / 2;
        this.camera.x = Math.max(0, Math.min(this.camera.x, this.levelWidth - this.width));
    }
    
    render() {
        this.ctx.clearRect(0, 0, this.width, this.height);
        
        this.renderBackground();
        
        this.ctx.save();
        this.ctx.translate(-this.camera.x, -this.camera.y);
        
        this.platforms.forEach(platform => platform.render());
        this.collectibles.forEach(item => item.render());
        this.enemies.forEach(enemy => enemy.render());
        this.mario.render();
        this.particles.forEach(particle => particle.render());
        
        this.ctx.restore();
        
        if (this.gameState === 'playing') {
            this.updateUI();
        }
    }
    
    renderBackground() {
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.height);
        gradient.addColorStop(0, '#87CEEB');
        gradient.addColorStop(1, '#98FB98');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        for (let i = 0; i < 20; i++) {
            const x = (i * 100 - this.camera.x * 0.1) % this.width;
            const y = 50 + Math.sin(i) * 20;
            this.ctx.fillRect(x, y, 60, 20);
        }
    }
    
    updateUI() {
        document.getElementById('scoreValue').textContent = this.score;
        document.getElementById('livesValue').textContent = this.lives;
        document.getElementById('coinsValue').textContent = this.coins;
    }
    
    addScore(points) {
        this.score += points;
    }
    
    collectCoin() {
        this.coins++;
        this.addScore(100);
    }
    
    loseLife() {
        this.lives--;
        if (this.lives <= 0) {
            this.gameOver();
        } else {
            this.mario = new Mario(100, 400, this);
            this.camera.x = 0;
        }
    }
    
    gameOver() {
        this.gameState = 'gameOver';
        this.soundManager.play('gameOver');
        document.getElementById('finalScore').textContent = this.score;
        document.getElementById('gameOver').classList.remove('hidden');
    }
    
    winLevel() {
        this.addScore(1000);
        alert('Congratulations! You completed the level!');
        this.restartGame();
    }
    
    createParticles(x, y, color, count = 5) {
        for (let i = 0; i < count; i++) {
            this.particles.push(new Particle(x, y, color, this));
        }
    }
}

class Mario {
    constructor(x, y, game) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.width = 32;
        this.height = 32;
        this.velocityX = 0;
        this.velocityY = 0;
        this.onGround = false;
        this.maxSpeed = 5;
        this.jumpPower = -15;
        this.big = false;
        this.invulnerable = false;
        this.invulnerabilityTime = 0;
        this.direction = 1;
    }
    
    update() {
        this.handleInput();
        this.applyPhysics();
        this.checkCollisions();
        
        if (this.invulnerable) {
            this.invulnerabilityTime--;
            if (this.invulnerabilityTime <= 0) {
                this.invulnerable = false;
            }
        }
    }
    
    handleInput() {
        const keys = this.game.keys;
        
        if (keys['KeyA'] || keys['ArrowLeft']) {
            this.velocityX = Math.max(this.velocityX - 0.5, -this.maxSpeed);
            this.direction = -1;
        } else if (keys['KeyD'] || keys['ArrowRight']) {
            this.velocityX = Math.min(this.velocityX + 0.5, this.maxSpeed);
            this.direction = 1;
        } else {
            this.velocityX *= this.game.friction;
        }
        
        if ((keys['KeyW'] || keys['ArrowUp'] || keys['Space']) && this.onGround) {
            this.game.soundManager.play('jump');
            this.velocityY = this.jumpPower;
            this.onGround = false;
        }
    }
    
    applyPhysics() {
        this.velocityY += this.game.gravity;
        this.x += this.velocityX;
        this.y += this.velocityY;
        
        if (this.x < 0) this.x = 0;
        if (this.x > this.game.levelWidth - this.width) {
            this.x = this.game.levelWidth - this.width;
        }
    }
    
    checkCollisions() {
        this.onGround = false;
        
        this.game.platforms.forEach(platform => {
            if (this.collidesWith(platform)) {
                if (this.velocityY > 0 && this.y < platform.y) {
                    this.y = platform.y - this.height;
                    this.velocityY = 0;
                    this.onGround = true;
                } else if (this.velocityY < 0 && this.y > platform.y) {
                    this.y = platform.y + platform.height;
                    this.velocityY = 0;
                } else if (this.velocityX > 0) {
                    this.x = platform.x - this.width;
                    this.velocityX = 0;
                } else if (this.velocityX < 0) {
                    this.x = platform.x + platform.width;
                    this.velocityX = 0;
                }
            }
        });
        
        this.game.enemies.forEach(enemy => {
            if (this.collidesWith(enemy) && !enemy.destroyed && !this.invulnerable) {
                if (this.velocityY > 0 && this.y < enemy.y - 10) {
                    enemy.destroy();
                    this.velocityY = -8;
                    this.game.addScore(200);
                    this.game.soundManager.play('stomp');
                    this.game.createParticles(enemy.x + enemy.width/2, enemy.y + enemy.height/2, '#8B4513');
                } else {
                    this.takeDamage();
                }
            }
        });
        
        this.game.collectibles.forEach(item => {
            if (this.collidesWith(item) && !item.collected) {
                item.collect();
            }
        });
    }
    
    collidesWith(object) {
        return this.x < object.x + object.width &&
               this.x + this.width > object.x &&
               this.y < object.y + object.height &&
               this.y + this.height > object.y;
    }
    
    takeDamage() {
        if (this.big) {
            this.big = false;
            this.height = 32;
            this.invulnerable = true;
            this.invulnerabilityTime = 120;
        } else {
            this.game.loseLife();
        }
    }
    
    powerUp() {
        if (!this.big) {
            this.big = true;
            this.height = 48;
            this.y -= 16;
        }
    }
    
    render() {
        const ctx = this.game.ctx;
        
        if (this.invulnerable && Math.floor(this.invulnerabilityTime / 5) % 2) {
            return;
        }
        
        ctx.fillStyle = this.big ? '#FF6B35' : '#FF0000';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(this.x + 4, this.y + 4, this.width - 8, 8);
        
        ctx.fillStyle = '#FFE4C4';
        ctx.fillRect(this.x + 8, this.y + 12, this.width - 16, 12);
        
        ctx.fillStyle = '#000';
        ctx.fillRect(this.x + 10, this.y + 14, 4, 4);
        ctx.fillRect(this.x + 18, this.y + 14, 4, 4);
        
        ctx.fillStyle = '#0000FF';
        ctx.fillRect(this.x + 6, this.y + this.height - 16, this.width - 12, 8);
    }
}

class Platform {
    constructor(x, y, width, height, game) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
    
    render() {
        const ctx = this.game.ctx;
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        ctx.fillStyle = '#90EE90';
        ctx.fillRect(this.x, this.y - 5, this.width, 5);
        
        for (let i = 0; i < this.width; i += 20) {
            ctx.fillStyle = '#654321';
            ctx.fillRect(this.x + i, this.y + 5, 2, this.height - 10);
        }
    }
}

class Goomba {
    constructor(x, y, game) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.width = 24;
        this.height = 24;
        this.velocityX = -1;
        this.destroyed = false;
        this.onGround = false;
    }
    
    update() {
        if (this.destroyed) return;
        
        this.x += this.velocityX;
        this.y += this.game.gravity;
        
        this.onGround = false;
        this.game.platforms.forEach(platform => {
            if (this.collidesWith(platform)) {
                if (this.y < platform.y) {
                    this.y = platform.y - this.height;
                    this.onGround = true;
                } else if (this.velocityX > 0) {
                    this.x = platform.x - this.width;
                    this.velocityX = -Math.abs(this.velocityX);
                } else if (this.velocityX < 0) {
                    this.x = platform.x + platform.width;
                    this.velocityX = Math.abs(this.velocityX);
                }
            }
        });
        
        if (this.y > this.game.height) {
            this.destroyed = true;
        }
    }
    
    collidesWith(object) {
        return this.x < object.x + object.width &&
               this.x + this.width > object.x &&
               this.y < object.y + object.height &&
               this.y + this.height > object.y;
    }
    
    destroy() {
        this.destroyed = true;
    }
    
    render() {
        if (this.destroyed) return;
        
        const ctx = this.game.ctx;
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        ctx.fillStyle = '#000';
        ctx.fillRect(this.x + 4, this.y + 4, 4, 4);
        ctx.fillRect(this.x + 16, this.y + 4, 4, 4);
        
        ctx.fillStyle = '#654321';
        ctx.fillRect(this.x + 2, this.y + this.height - 8, this.width - 4, 4);
    }
}

class Coin {
    constructor(x, y, game) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.width = 16;
        this.height = 16;
        this.collected = false;
        this.rotation = 0;
    }
    
    update() {
        this.rotation += 0.1;
    }
    
    collect() {
        this.collected = true;
        this.game.collectCoin();
        this.game.soundManager.play('coin');
        this.game.createParticles(this.x + this.width/2, this.y + this.height/2, '#FFD700');
    }
    
    render() {
        if (this.collected) return;
        
        const ctx = this.game.ctx;
        const centerX = this.x + this.width / 2;
        const centerY = this.y + this.height / 2;
        
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(this.rotation);
        
        ctx.fillStyle = '#FFD700';
        ctx.fillRect(-this.width/2, -this.height/2, this.width, this.height);
        
        ctx.fillStyle = '#FFA500';
        ctx.fillRect(-this.width/2 + 2, -this.height/2 + 2, this.width - 4, this.height - 4);
        
        ctx.restore();
    }
}

class PowerUp {
    constructor(x, y, game) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.width = 20;
        this.height = 20;
        this.collected = false;
        this.velocityY = -2;
    }
    
    update() {
        this.y += this.velocityY;
        this.velocityY += 0.1;
        
        if (this.y > this.game.height) {
            this.collected = true;
        }
    }
    
    collect() {
        this.collected = true;
        this.game.mario.powerUp();
        this.game.addScore(500);
        this.game.soundManager.play('powerup');
        this.game.createParticles(this.x + this.width/2, this.y + this.height/2, '#FF69B4');
    }
    
    render() {
        if (this.collected) return;
        
        const ctx = this.game.ctx;
        ctx.fillStyle = '#FF69B4';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        ctx.fillStyle = '#FFF';
        ctx.fillRect(this.x + 2, this.y + 2, this.width - 4, this.height - 4);
        
        ctx.fillStyle = '#FF1493';
        ctx.fillRect(this.x + 6, this.y + 6, this.width - 12, this.height - 12);
    }
}

class Particle {
    constructor(x, y, color, game) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.velocityX = (Math.random() - 0.5) * 8;
        this.velocityY = (Math.random() - 0.5) * 8 - 2;
        this.color = color;
        this.life = 30;
        this.maxLife = 30;
        this.size = Math.random() * 4 + 2;
    }
    
    update() {
        this.x += this.velocityX;
        this.y += this.velocityY;
        this.velocityY += 0.3;
        this.life--;
    }
    
    render() {
        const ctx = this.game.ctx;
        const alpha = this.life / this.maxLife;
        
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.size, this.size);
        ctx.restore();
    }
}

window.addEventListener('load', () => {
    new Game();
});
