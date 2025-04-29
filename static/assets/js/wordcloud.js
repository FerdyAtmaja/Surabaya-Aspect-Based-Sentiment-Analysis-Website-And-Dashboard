document.addEventListener("DOMContentLoaded", function () {
  // Load available years
  fetch("/get_available_years")
    .then((response) => response.json())
    .then((data) => {
      const yearSelect = document.getElementById("yearSelect");
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
    });

  // Load available aspects
  function loadAspects(year) {
    fetch(`/get_aspects/${year}`)
      .then((response) => response.json())
      .then((data) => {
        const aspectSelect = document.getElementById("aspectSelect");
        // Clear previous options except "All Aspects"
        aspectSelect.innerHTML = '<option value="all">All Aspects</option>';

        data.aspects.forEach((aspect) => {
          const option = document.createElement("option");
          option.value = aspect;
          option.textContent = aspect;
          aspectSelect.appendChild(option);
        });
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
  fetch(`/get_wordcloud_data/${year}/${aspect}`)
    .then((response) => response.json())
    .then((data) => {
      updateStatistics(data.statistics);
      updateWordCloud("positiveWordCloud", data.positive_words, "#4CAF50");
      updateWordCloud("negativeWordCloud", data.negative_words, "#FF5252");
    });
}

function updateStatistics(stats) {
  document.getElementById("totalComplaints").textContent = stats.total;
  document.getElementById("positiveCount").textContent = stats.positive;
  document.getElementById("negativeCount").textContent = stats.negative;
}

function updateWordCloud(elementId, words, color) {
  if (!words || words.length === 0) {
    document.getElementById(elementId).innerHTML =
      '<p class="text-center mt-5">No data available</p>';
    return;
  }

  const options = {
    list: words.map((word) => [word.text, word.weight]),
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

  WordCloud(document.getElementById(elementId), options);
}
