'use strict';

document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('background-audio');
    const btn = document.getElementById('toggle-music');

    if (!audio || !btn) {
        console.error('Audio element or toggle button not found!');
        return;
    }

    function updateMusicButton(isOn) {
        btn.textContent = isOn ? '🔊 Désactiver la musique' : '🔇 Activer la musique';
    }

    function getMusicState() {
        const stored = localStorage.getItem('musicOn');
        return stored === null ? true : stored === 'true';
    }

    function setMusicState(isOn) {
        localStorage.setItem('musicOn', isOn);
        updateMusicButton(isOn);
        if (isOn) {
            audio.play().catch(() => {});
        } else {
            audio.pause();
        }
    }

    let musicOn = getMusicState();
    setMusicState(musicOn);

    btn.addEventListener('click', () => {
        musicOn = !musicOn;
        setMusicState(musicOn);
    });
});
