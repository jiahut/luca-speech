document.addEventListener('DOMContentLoaded', () => {
    const audioSelect = document.getElementById('audio-select');
    const audioPlayer = document.getElementById('audio-player');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const loopBtn = document.getElementById('loop-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Fetch audio files and populate the dropdown
    fetch('/api/audio-files')
        .then(response => response.json())
        .then(files => {
            files.forEach(file => {
                const option = document.createElement('option');
                option.value = file;
                option.textContent = file;
                audioSelect.appendChild(option);
            });
            // Load the first file by default
            if (files.length > 0) {
                audioPlayer.src = `output/${files[0]}`;
            }
        })
        .catch(error => console.error('Error fetching audio files:', error));

    // Event listener for file selection
    audioSelect.addEventListener('change', () => {
        const selectedFile = audioSelect.value;
        if (selectedFile) {
            audioPlayer.src = `output/${selectedFile}`;
            playPauseBtn.textContent = 'Play';
        }
    });

    // Event listener for play/pause button
    playPauseBtn.addEventListener('click', () => {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playPauseBtn.textContent = 'Pause';
        } else {
            audioPlayer.pause();
            playPauseBtn.textContent = 'Play';
        }
    });

    // Event listener for audio element play/pause
    audioPlayer.addEventListener('play', () => {
        playPauseBtn.textContent = 'Pause';
    });

    audioPlayer.addEventListener('pause', () => {
        playPauseBtn.textContent = 'Play';
    });

    // Event listener for loop button
    loopBtn.addEventListener('click', () => {
        audioPlayer.loop = !audioPlayer.loop;
        loopBtn.textContent = `Loop: ${audioPlayer.loop ? 'On' : 'Off'}`;
    });

    // Event listeners for speed control buttons
    speedBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            audioPlayer.playbackRate = parseFloat(btn.dataset.speed);
        });
    });
});
