document.addEventListener('DOMContentLoaded', () => {
  const mainForm = document.getElementById('mainForm');
  const modeRadios = document.getElementsByName('mode');
  const manualFields = document.getElementById('manualFields');
  const autoFields = document.getElementById('autoFields');
  const autoCompleteBtn = document.getElementById('autoCompleteBtn');
  const messageDiv = document.getElementById('message');
  const themeToggle = document.getElementById('themeToggle');
  const loadingScreen = document.getElementById('loadingScreen');
  console.log("Loading screen; ",loadingScreen);
  // Auto mode counters
  const countdownTimerElem = document.getElementById('countdownTimer');
  const autoTweetCountElem = document.getElementById('autoTweetCount');
  let countdownInterval = null;
  let autoIntervalValue = 0; // seconds

  // Toggle between Manual and Auto modes for single tweet
  modeRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      if (radio.value === 'auto' && radio.checked) {
        manualFields.style.display = 'none';
        autoFields.style.display = 'block';
        // If interval is set, start the countdown
        const intervalInput = document.getElementById('interval');
        if (intervalInput && intervalInput.value) {
          autoIntervalValue = parseInt(intervalInput.value);
          startCountdown(autoIntervalValue);
        }
      } else {
        manualFields.style.display = 'block';
        autoFields.style.display = 'none';
        clearInterval(countdownInterval);
      }
    });
  });

  // Dark/Light mode toggle
  if (themeToggle) {
    themeToggle.addEventListener('change', () => {
      document.body.classList.toggle('dark-mode', themeToggle.checked);
    });
  }

  // Auto-complete button functionality
  if (autoCompleteBtn) {
    autoCompleteBtn.addEventListener('click', async () => {
      console.log("Auto-complete button clicked...");
      try {
        if (loadingScreen) loadingScreen.style.display = 'flex'; // Show loading screen

        const titleElem = document.getElementById('title');
        const contentElem = document.getElementById('content');
        const hashtagsElem = document.getElementById('hashtags');

        const title = titleElem ? titleElem.value : '';
        const content = contentElem ? contentElem.value : '';
        const hashtags = hashtagsElem ? hashtagsElem.value : '';

        const response = await fetch(`/generate_tweets?title=${encodeURIComponent(title)}&content=${encodeURIComponent(content)}&hashtags=${encodeURIComponent(hashtags)}`);

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (titleElem) titleElem.value = data.title;
        if (contentElem) contentElem.value = data.content;
        if (hashtagsElem) hashtagsElem.value = data.hashtags.join(', ');

      } catch (error) {
        console.error('Error fetching AI tweet:', error);
        messageDiv.innerText = 'Error fetching AI-generated tweet!';
      } finally {
        if (loadingScreen) loadingScreen.style.display = 'none'; // Hide loading screen
      }
    });
  } else {
    console.warn("Auto-complete button not found!");
  }

  // Start countdown timer for auto tweet posting
  function startCountdown(intervalSec) {
    let remaining = intervalSec;
    countdownTimerElem.textContent = remaining;
    clearInterval(countdownInterval);
    countdownInterval = setInterval(() => {
      remaining--;
      if (remaining <= 0) {
        remaining = intervalSec;
      }
      countdownTimerElem.textContent = remaining;
    }, 1000);
  }

  // Poll backend for auto tweet count every 5 seconds
  async function updateAutoTweetCount() {
    try {
      const response = await fetch('/auto_count');
      const data = await response.json();
      autoTweetCountElem.textContent = data.auto_tweet_count;
    } catch (error) {
      console.error('Error fetching auto tweet count:', error);
    }
  }
  setInterval(updateAutoTweetCount, 5000);

  // Form submission handling
  if (mainForm) {
    mainForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        if (loadingScreen) loadingScreen.style.display = 'flex'; // Show loading screen

        // For auto mode, update the countdown based on the interval
        const mode = document.querySelector('input[name="mode"]:checked').value;
        if (mode === 'auto') {
          const intervalInput = document.getElementById('interval');
          if (intervalInput && intervalInput.value) {
            autoIntervalValue = parseInt(intervalInput.value);
            startCountdown(autoIntervalValue);
          }
        }

        const formData = new FormData(mainForm);
        const response = await fetch('/post_tweet', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();
        messageDiv.innerText = result.message;

      } catch (error) {
        console.error('Error posting tweet:', error);
        messageDiv.innerText = 'Error posting tweet!';
      } finally {
        if (loadingScreen) loadingScreen.style.display = 'none'; // Hide loading screen
      }
    });
  }
});
