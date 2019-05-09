<script>
import { Pie } from 'vue-chartjs'

export default {
  name:"Piechart",
  extends: Pie,
  props: [
    'data',
    'name'
  ],
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Teen','Big','Japanese','Nurse'],
      datasets: [
        {
          label: this.name,
          backgroundColor: ['#f8979', '#eee','#ddd','#888'],
          data: this.data
        }
      ]
    })
  }
}
</script>
