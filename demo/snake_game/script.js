class MatrixRain {
    constructor() {
        this.createMatrixRain();
    }
    
    createMatrixRain() {
        const matrixContainer = document.createElement('div');
        matrixContainer.className = 'matrix-rain';
        document.body.appendChild(matrixContainer);
        
        const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        const numColumns = Math.floor(window.innerWidth / 20);
        
        for (let i = 0; i < numColumns; i++) {
            const column = document.createElement('div');
            column.className = 'matrix-column';
            column.style.left = `${i * 20}px`;
            column.style.animationDuration = `${Math.random() * 3 + 2}s`;
            column.style.animationDelay = `${Math.random() * 2}s`;
            
            let columnText = '';
            const columnHeight = Math.floor(Math.random() * 20) + 10;
            
            for (let j = 0; j < columnHeight; j++) {
                const char = chars[Math.floor(Math.random() * chars.length)];
                const opacity = Math.max(0.1, (columnHeight - j) / columnHeight);
                columnText += `<span class="matrix-char" style="opacity: ${opacity}">${char}</span><br>`;
            }
            
            column.innerHTML = columnText;
            matrixContainer.appendChild(column);
        }
        
        setTimeout(() => {
            matrixContainer.remove();
            this.createMatrixRain();
        }, 8000);
    }
}

class SnakeGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.scoreElement = document.getElementById('score');
        this.highScoreElement = document.getElementById('highScore');
        this.levelElement = document.getElementById('level');
        this.gameOverElement = document.getElementById('gameOver');
        this.pausedElement = document.getElementById('paused');
        this.finalScoreElement = document.getElementById('finalScore');
        this.statusElement = document.getElementById('gameStatus');
        
        this.gridSize = 20;
        this.canvas.width = 600;
        this.canvas.height = 400;
        this.cols = this.canvas.width / this.gridSize;
        this.rows = this.canvas.height / this.gridSize;
        
        this.reset();
        this.setupEventListeners();
        this.loadHighScore();
        this.gameLoop();
        this.addMatrixEffects();
    }
    
    addMatrixEffects() {
        new MatrixRain();
        
        setInterval(() => {
            this.glitchScore();
        }, 5000);
    }
    
    glitchScore() {
        if (this.gameRunning && !this.gameOver && !this.paused) {
            const originalScore = this.scoreElement.textContent;
            const glitchChars = '!@#$%^&*()_+-=[]{}|;:,.<>?';
            
            for (let i = 0; i < 3; i++) {
                setTimeout(() => {
                    if (i < 2) {
                        let glitched = '';
                        for (let j = 0; j < 4; j++) {
                            glitched += glitchChars[Math.floor(Math.random() * glitchChars.length)];
                        }
                        this.scoreElement.textContent = glitched;
                    } else {
                        this.scoreElement.textContent = originalScore;
                    }
                }, i * 100);
            }
        }
    }
    
    reset() {
        this.snake = [{ x: 10, y: 10 }];
        this.direction = { x: 0, y: 0 };
        this.food = this.generateFood();
        this.score = 0;
        this.level = 1;
        this.gameRunning = false;
        this.gameOver = false;
        this.paused = false;
        this.baseSpeed = 150;
        this.speed = this.baseSpeed;
        this.lastMoveTime = 0;
        
        this.updateDisplay();
        this.hideOverlays();
        this.updateStatus('SYSTEM READY - AWAITING INPUT...');
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            this.handleKeyPress(e);
        });
        
        document.addEventListener('keyup', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
            }
        });
    }
    
    handleKeyPress(e) {
        const key = e.code;
        
        if (key === 'Space') {
            e.preventDefault();
            this.togglePause();
            return;
        }
        
        if (key === 'KeyR' && (this.gameOver || this.paused)) {
            this.reset();
            return;
        }
        
        if (this.gameOver || this.paused) return;
        
        const directions = {
            'ArrowUp': { x: 0, y: -1 },
            'ArrowDown': { x: 0, y: 1 },
            'ArrowLeft': { x: -1, y: 0 },
            'ArrowRight': { x: 1, y: 0 },
            'KeyW': { x: 0, y: -1 },
            'KeyS': { x: 0, y: 1 },
            'KeyA': { x: -1, y: 0 },
            'KeyD': { x: 1, y: 0 }
        };
        
        const newDirection = directions[key];
        if (newDirection) {
            if (!this.gameRunning) {
                this.gameRunning = true;
                this.updateStatus('MATRIX PROTOCOL ACTIVE...');
            }
            
            if (this.direction.x === 0 && this.direction.y === 0) {
                this.direction = newDirection;
            } else if (
                newDirection.x !== -this.direction.x ||
                newDirection.y !== -this.direction.y
            ) {
                this.direction = newDirection;
            }
        }
    }
    
    togglePause() {
        if (this.gameOver) {
            this.reset();
            return;
        }
        
        if (!this.gameRunning) return;
        
        this.paused = !this.paused;
        if (this.paused) {
            this.showPaused();
            this.updateStatus('SYSTEM SUSPENDED');
        } else {
            this.hidePaused();
            this.updateStatus('MATRIX PROTOCOL ACTIVE...');
        }
    }
    
    generateFood() {
        let food;
        do {
            food = {
                x: Math.floor(Math.random() * this.cols),
                y: Math.floor(Math.random() * this.rows)
            };
        } while (this.isSnakePosition(food.x, food.y));
        return food;
    }
    
    isSnakePosition(x, y) {
        return this.snake.some(segment => segment.x === x && segment.y === y);
    }
    
    update(currentTime) {
        if (!this.gameRunning || this.gameOver || this.paused) return;
        
        if (currentTime - this.lastMoveTime < this.speed) return;
        this.lastMoveTime = currentTime;
        
        if (this.direction.x === 0 && this.direction.y === 0) return;
        
        const head = { ...this.snake[0] };
        head.x += this.direction.x;
        head.y += this.direction.y;
        
        if (this.checkCollision(head)) {
            this.endGame();
            return;
        }
        
        this.snake.unshift(head);
        
        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 10;
            this.food = this.generateFood();
            this.updateLevel();
            this.updateDisplay();
            this.updateStatus('DATA PACKET ACQUIRED...');
        } else {
            this.snake.pop();
        }
    }
    
    checkCollision(head) {
        if (head.x < 0 || head.x >= this.cols || 
            head.y < 0 || head.y >= this.rows) {
            return true;
        }
        
        return this.snake.some(segment => 
            segment.x === head.x && segment.y === head.y
        );
    }
    
    updateLevel() {
        const newLevel = Math.floor(this.score / 50) + 1;
        if (newLevel > this.level) {
            this.level = newLevel;
            this.speed = Math.max(50, this.baseSpeed - (this.level - 1) * 15);
            this.updateStatus(`LEVEL ${this.level} - PROTOCOL ENHANCED`);
        }
    }
    
    endGame() {
        this.gameOver = true;
        this.gameRunning = false;
        this.updateHighScore();
        this.showGameOver();
        this.updateStatus('MATRIX BREACH - SYSTEM COMPROMISED');
    }
    
    updateHighScore() {
        const currentHigh = parseInt(localStorage.getItem('matrixSnakeHighScore') || '0');
        if (this.score > currentHigh) {
            localStorage.setItem('matrixSnakeHighScore', this.score.toString());
            this.highScoreElement.textContent = this.score.toString().padStart(4, '0');
        }
    }
    
    loadHighScore() {
        const highScore = parseInt(localStorage.getItem('matrixSnakeHighScore') || '0');
        this.highScoreElement.textContent = highScore.toString().padStart(4, '0');
    }
    
    updateDisplay() {
        this.scoreElement.textContent = this.score.toString().padStart(4, '0');
        this.levelElement.textContent = this.level.toString().padStart(2, '0');
        this.finalScoreElement.textContent = this.score.toString();
    }
    
    updateStatus(message) {
        this.statusElement.textContent = message;
    }
    
    showGameOver() {
        this.gameOverElement.classList.remove('hidden');
    }
    
    showPaused() {
        this.pausedElement.classList.remove('hidden');
    }
    
    hidePaused() {
        this.pausedElement.classList.add('hidden');
    }
    
    hideOverlays() {
        this.gameOverElement.classList.add('hidden');
        this.pausedElement.classList.add('hidden');
    }
    
    render() {
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.renderMatrixGrid();
        this.renderFood();
        this.renderSnake();
    }
    
    renderMatrixGrid() {
        this.ctx.strokeStyle = '#003300';
        this.ctx.lineWidth = 0.5;
        this.ctx.shadowColor = '#00ff41';
        this.ctx.shadowBlur = 1;
        
        for (let x = 0; x <= this.canvas.width; x += this.gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.canvas.height; y += this.gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
        
        this.ctx.shadowBlur = 0;
    }
    
    renderFood() {
        const x = this.food.x * this.gridSize;
        const y = this.food.y * this.gridSize;
        
        this.ctx.fillStyle = '#ff0033';
        this.ctx.shadowColor = '#ff0033';
        this.ctx.shadowBlur = 15;
        this.ctx.fillRect(x + 2, y + 2, this.gridSize - 4, this.gridSize - 4);
        
        this.ctx.fillStyle = '#ff3355';
        this.ctx.shadowBlur = 8;
        this.ctx.fillRect(x + 4, y + 4, this.gridSize - 8, this.gridSize - 8);
        
        this.ctx.fillStyle = '#ff6677';
        this.ctx.shadowBlur = 0;
        this.ctx.fillRect(x + 6, y + 6, this.gridSize - 12, this.gridSize - 12);
    }
    
    renderSnake() {
        this.snake.forEach((segment, index) => {
            const x = segment.x * this.gridSize;
            const y = segment.y * this.gridSize;
            
            if (index === 0) {
                this.ctx.fillStyle = '#00ff41';
                this.ctx.shadowColor = '#00ff41';
                this.ctx.shadowBlur = 20;
                this.ctx.fillRect(x + 1, y + 1, this.gridSize - 2, this.gridSize - 2);
                
                this.ctx.fillStyle = '#44ff77';
                this.ctx.shadowBlur = 10;
                this.ctx.fillRect(x + 3, y + 3, this.gridSize - 6, this.gridSize - 6);
                
                this.ctx.fillStyle = '#88ffaa';
                this.ctx.shadowBlur = 0;
                this.ctx.fillRect(x + 5, y + 5, this.gridSize - 10, this.gridSize - 10);
            } else {
                const intensity = Math.max(0.2, 1 - (index * 0.08));
                this.ctx.fillStyle = `rgba(0, 255, 65, ${intensity})`;
                this.ctx.shadowColor = '#00ff41';
                this.ctx.shadowBlur = 8 * intensity;
                this.ctx.fillRect(x + 1, y + 1, this.gridSize - 2, this.gridSize - 2);
                
                if (intensity > 0.5) {
                    this.ctx.fillStyle = `rgba(68, 255, 119, ${intensity * 0.7})`;
                    this.ctx.shadowBlur = 4 * intensity;
                    this.ctx.fillRect(x + 3, y + 3, this.gridSize - 6, this.gridSize - 6);
                }
            }
        });
        this.ctx.shadowBlur = 0;
    }
    
    gameLoop(currentTime = 0) {
        this.update(currentTime);
        this.render();
        requestAnimationFrame((time) => this.gameLoop(time));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SnakeGame();
});
