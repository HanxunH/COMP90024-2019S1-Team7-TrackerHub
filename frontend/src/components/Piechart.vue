<script>
import { Pie } from 'vue-chartjs'

export default {
  name:"Piechart",
  extends: Pie,
  props: [
    'name',
    'pieData'
  ],
  mounted () {
    console.log(this.pieData)
    // Overwriting base render method with actual data.
    this.renderChart(this.pieData)
  }
}
</script>
