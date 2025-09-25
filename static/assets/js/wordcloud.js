document.addEventListener("DOMContentLoaded", function () {
  // Load available years
  fetch("/get_available_years")
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      const yearSelect = document.getElementById("yearSelect");
      if (data && data.years) {
        data.years.forEach((year) => {
          const option = document.createElement("option");
          option.value = year;
          option.textContent = year;
          yearSelect.appendChild(option);
        });

        // Load initial data for first year
        if (data.years.length > 0) {
          yearSelect.value = data.years[0];
          loadAspects(data.years[0]);
          loadWordCloudData(data.years[0], "all");
        }
      }
    })
    .catch((error) => {
      console.error('Error loading years:', error);
      showError('Failed to load available years');
    });

  // Load available aspects
  function loadAspects(year) {
    // Validate year input
    if (!year || isNaN(year)) {
      console.error('Invalid year provided');
      return;
    }
    
    fetch(`/get_aspects/${encodeURIComponent(year)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        const aspectSelect = document.getElementById("aspectSelect");
        if (aspectSelect && data && data.aspects) {
          // Clear previous options except "All Aspects"
          aspectSelect.innerHTML = '<option value="all">All Aspects</option>';

          data.aspects.forEach((aspect) => {
            const option = document.createElement("option");
            option.value = aspect;
            option.textContent = aspect;
            aspectSelect.appendChild(option);
          });
        }
      })
      .catch((error) => {
        console.error('Error loading aspects:', error);
        showError('Failed to load aspects');
      });
  }

  // Year change event
  document
    .getElementById("yearSelect")
    .addEventListener("change", function (e) {
      const year = e.target.value;
      loadAspects(year);
      loadWordCloudData(year, document.getElementById("aspectSelect").value);
    });

  // Aspect change event
  document
    .getElementById("aspectSelect")
    .addEventListener("change", function (e) {
      const year = document.getElementById("yearSelect").value;
      loadWordCloudData(year, e.target.value);
    });
});

function loadWordCloudData(year, aspect) {
  // Validate inputs
  if (!year || !aspect) {
    console.error('Invalid year or aspect provided');
    return;
  }
  
  fetch(`/get_wordcloud_data/${encodeURIComponent(year)}/${encodeURIComponent(aspect)}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      if (data) {
        updateStatistics(data.statistics);
        updateWordCloud("positiveWordCloud", data.positive_words, "#4CAF50");
        updateWordCloud("negativeWordCloud", data.negative_words, "#FF5252");
      }
    })
    .catch((error) => {
      console.error('Error loading wordcloud data:', error);
      showError('Failed to load wordcloud data');
    });
}

function updateStatistics(stats) {
  if (!stats || typeof stats !== 'object') {
    console.error('Invalid stats data provided');
    return;
  }
  
  const totalElement = document.getElementById("totalComplaints");
  const positiveElement = document.getElementById("positiveCount");
  const negativeElement = document.getElementById("negativeCount");
  
  if (totalElement) totalElement.textContent = stats.total || 0;
  if (positiveElement) positiveElement.textContent = stats.positive || 0;
  if (negativeElement) negativeElement.textContent = stats.negative || 0;
}

function updateWordCloud(elementId, words, color) {
  const element = document.getElementById(elementId);
  if (!element) {
    console.error('Element not found:', elementId);
    return;
  }
  
  if (!words || words.length === 0) {
    element.textContent = 'No data available';
    return;
  }

  // Sanitize and validate word data
  const sanitizedWords = words.filter(word => 
    word && typeof word.text === 'string' && typeof word.weight === 'number'
  ).map(word => [word.text.replace(/[<>"'&]/g, ''), Math.max(0, word.weight)]);

  if (sanitizedWords.length === 0) {
    element.textContent = 'No valid data available';
    return;
  }

  const options = {
    list: sanitizedWords,
    gridSize: 16,
    weightFactor: function (size) {
      return Math.pow(size, 2.3) * 1;
    },
    fontFamily: "Inter, sans-serif",
    color: color,
    rotateRatio: 0.5,
    rotationSteps: 2,
    backgroundColor: "transparent",
    minSize: 10,
  };

  try {
    WordCloud(element, options);
  } catch (error) {
    console.error('Error creating wordcloud:', error);
    element.textContent = 'Error generating wordcloud';
  }
}

function showError(message) {
  // Sanitize message input
  if (!message || typeof message !== 'string') {
    message = 'An error occurred';
  }
  
  // Remove any HTML tags for security
  const sanitizedMessage = message.replace(/<[^>]*>/g, '').substring(0, 200);
  
  const errorDiv = document.createElement('div');
  errorDiv.className = 'alert alert-danger';
  errorDiv.textContent = sanitizedMessage;
  document.body.insertBefore(errorDiv, document.body.firstChild);
  
  setTimeout(() => {
    if (errorDiv.parentNode) {
      errorDiv.parentNode.removeChild(errorDiv);
    }
  }, 5000);
}
