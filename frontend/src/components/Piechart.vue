<script>
import { Pie } from 'vue-chartjs'

export default {
  name:"Piechart",
  extends: Pie,
  props: [
    'data'
  ],
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Teen','Big','Japanese','Nurse'],
      datasets: [
        {
          label: 'PornHub Commits',
          backgroundColor: ['#f8979', '#eee','#ddd','#888'],
          data: this.data
        }
      ]
    })
  }
}
</script>
