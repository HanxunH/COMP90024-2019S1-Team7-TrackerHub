<style lang="less" scoped="scoped">
@import '../assets/css/common.less';
</style>
<template>
	<div class="page-index">
		
	</div>
</template>

<script>
export default {
	name: 'home',
    components: {},
    data () {
    	return {}
    },
    methods: {
    	getData(){
    		this.$ajax({
				method: 'GET', 
				url: 'melbourneGeoInfo.json', 
				data: {},
			}).then(res => {
        console.log(res)
			}, error => {
        console.log('error')
	        })
    	}
    },
    created () {},
	mounted(){
		
	}
}
</script>
