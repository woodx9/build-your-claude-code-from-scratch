class SoundManager {
    constructor() {
        this.audioContext = null;
        this.sounds = {};
        this.muted = false;
        this.volume = 0.3;
        this.init();
    }
    
    init() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.createSounds();
        } catch (e) {
            console.warn('Web Audio API not supported');
        }
    }
    
    createSounds() {
        this.sounds.jump = this.createTone(220, 0.1, 'sawtooth');
        this.sounds.coin = this.createTone(523, 0.15, 'sine');
        this.sounds.powerup = this.createChord([262, 330, 392], 0.3);
        this.sounds.stomp = this.createTone(110, 0.1, 'square');
        this.sounds.gameOver = this.createChord([147, 165, 185], 0.5);
    }
    
    createTone(frequency, duration, type = 'sine') {
        if (!this.audioContext) return null;
        
        return () => {
            if (this.muted) return;
            
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            oscillator.type = type;
            
            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(this.volume, this.audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration);
        };
    }
    
    createChord(frequencies, duration) {
        if (!this.audioContext) return null;
        
        return () => {
            if (this.muted) return;
            
            frequencies.forEach((freq, index) => {
                setTimeout(() => {
                    const oscillator = this.audioContext.createOscillator();
                    const gainNode = this.audioContext.createGain();
                    
                    oscillator.connect(gainNode);
                    gainNode.connect(this.audioContext.destination);
                    
                    oscillator.frequency.setValueAtTime(freq, this.audioContext.currentTime);
                    oscillator.type = 'sine';
                    
                    gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
                    gainNode.gain.linearRampToValueAtTime(this.volume * 0.5, this.audioContext.currentTime + 0.01);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
                    
                    oscillator.start(this.audioContext.currentTime);
                    oscillator.stop(this.audioContext.currentTime + duration);
                }, index * 50);
            });
        };
    }
    
    play(soundName) {
        if (this.sounds[soundName] && !this.muted) {
            this.sounds[soundName]();
        }
    }
    
    toggleMute() {
        this.muted = !this.muted;
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = SoundManager;
}
