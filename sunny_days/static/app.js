const {createApp} = Vue

createApp({
  data() {
    return {
      selectedCity: '',
      longestSunshinePeriod: null,
      monthMaxSunshinePeriod: null,
      currentSunshinePeriod: null,
    }
  },
  compilerOptions: {
    delimiters: ["@{", "}"]
  },
  created() {
    this.selectedCity = localStorage.getItem('selectedCity') || '';
    if (this.selectedCity) {
      this.getStatistics();
    }
  },
  watch: {
    selectedCity(newValue, oldValue) {
      localStorage.setItem('selectedCity', this.selectedCity);
      if (newValue) {
        this.getStatistics()
      }
    }
  },
  methods: {
    getStatistics() {
      fetch('/api/cities/' + this.selectedCity)
        .then(response => response.json())
        .then(data => {
          this.longestSunshinePeriod = data.longest_sunshine_period;
          this.monthMaxSunshinePeriod = data.month_max_sunshine_period;
          this.currentSunshinePeriod = data.current_sunshine_period;
          localStorage.setItem('selectedCity', this.selectedCity);
        });
    }
  }
}).mount('#app')