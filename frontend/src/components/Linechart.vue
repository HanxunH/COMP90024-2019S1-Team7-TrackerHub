<script>

import { Line } from 'vue-chartjs'
 
export default {
  name:"Linechart",
  extends: Line,
  props: [
    'data'
  ],
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      datasets: [
        {
          label: 'Github Commits',
          backgroundColor: '#f8979',
          data: [10, 30, 12, 39, 10, 40, 39, 20, 40, 70, 12, 11]
        }
      ]
    })
  }
}
</script>
