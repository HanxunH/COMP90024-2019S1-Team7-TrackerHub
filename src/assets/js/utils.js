function formatNum(m){
	m = Number(m)
	return m<10 ? '0'+m : m 
}
export default{
	minite2str (minutes) {
		let hour = Math.floor(minutes / 60)
		let minute = minutes % 60
		let timeStr = ''
		if (hour > 0) {
			timeStr += hour + 'hours'
		}
		if (minute > 0) {
			timeStr += minute + 'minutes'
		}
		return timeStr
	},
	ms2str (mseconds) {
		let msecs = Math.floor(mseconds/10)
		let m = Math.floor(msecs/(100*60))
		let s = Math.floor((msecs-m)/100)
		let ms = msecs%100
		return{
			minute: formatNum(m),
			second: formatNum(s),
			msecond: formatNum(ms)
		}
	},

	getUrlParam () {
		let searchArr = window.location.href.split('?')
		let search = searchArr.length > 1 ? searchArr[1].split('&') : []
		let param = {}
		if (search.length > 0 && search[0].length > 0) {
			search.forEach(item => {
				let temp = item.split('=')
				param[temp[0]] = temp[1]
			})
		}
		return param
	},
	
	// set localStorage
	setStorage (key, value) {
		if((typeof(value)).toLowerCase() == 'object'){
			value = JSON.stringify(value)
		}
		window.localStorage.setItem(key,value);
	},
	// get localStorage
	getStorage (key) {
		return window.localStorage.getItem(key);
	},
	// remove localStorage
	removeStorage (key) {
		window.localStorage.removeItem(key);
	},
	// clear localStorage
	clearStorage () {
		window.localStorage.clear();
	},

	// set cookie
	setCookie (cname, cvalue, exdays) {
		let d = new Date()
		d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000))
		let expires = 'expires=' + d.toUTCString()
		document.cookie = cname + '=' + cvalue + '; ' + expires
	},

	// get cookie
	getCookie (cname) {
		let name = cname + '='
		let ca = document.cookie.split(';')
		for (let i = 0; i < ca.length; i++) {
			let c = ca[i]
			while (c.charAt(0) === ' ') c = c.substring(1)
			if (c.indexOf(name) !== -1) return c.substring(name.length, c.length)
		}
		return null
	},

	// clear cookie
	clearCookie () {
		this.setCookie('username', '', -1)
	},
	formatNum(m){
		m = Number(m)
		return m<10 ? '0'+m : m 
	},
	//timestamp to dateTime
	timestamp2datetime(timestamp){
		var time = new Date(timestamp);
		var y = time.getFullYear();
		var m = time.getMonth()+1;
		var d = time.getDate();
		var h = time.getHours();
		var mm = time.getMinutes();
		var s = time.getSeconds();
		return y+'-'+formatNum(m)+'-'+formatNum(d)+' '+formatNum(h)+':'+formatNum(mm)+':'+formatNum(s);
	},
	// [TODO]: format date
	formatDate(date){
		var time = new Date(date);
		var y = time.getFullYear();
		var m = time.getMonth()+1;
		var d = time.getDate();
		return y+'-'+formatNum(m)+'-'+formatNum(d)
	},

	// remove Object From Array By properties
	removeObjFromArrayBy(arr, propObj){
		let key = Object.keys(propObj)[0]
		let value = propObj[key]
		let matchedObj = null
		for(let i = 0; i < arr.length; i++){
			if(arr[i][key] == value){
				matchedObj = {
					index: i,
					item: arr[i]
				}
				break;
			}
		}
		arr.splice(matchedObj.index,1)
		return arr
	},
	imageFile2DataURL(imageFile, maxWidth, maxHeight, quality=1.0, force){
		return new Promise((resolve, reject)=>{
			const reader = new FileReader(),
				oImg = new Image(),
				canvas = document.createElement('canvas'),
				context = canvas.getContext('2d');
			reader.onerror=reject
			oImg.onerror=reject
			oImg.onload = () => {
				let w,h
				if(force){
					w = maxWidth
					h = maxHeight
				}else{
					w = oImg.width
					h = oImg.height
					let	mw = maxWidth || w,
						mh = maxHeight || h,
						rate = Math.max(w/mw,h/mh)
					if(rate>1){
						w = w/rate
						h = h/rate
					}
				}
				canvas.width = w
				canvas.height = h
				context.clearRect(0, 0, w, h)
				context.drawImage(oImg, 0, 0, w, h)
				const dataURL = quality < 1 ? canvas.toDataURL('image/jpeg', quality) : canvas.toDataURL(imageFile.type)
				resolve(dataURL)
			}
			reader.onload= () => oImg.src = reader.result
			reader.readAsDataURL(imageFile)
		})
	},
	imageFileCompress(imageFile, maxWidth, maxHeight, quality, force){
		return this.imageFile2DataURL(imageFile, maxWidth, maxHeight, quality, force).then( dataURL => {
			// console.log(dataURL)
			// const newFile = dataURLtoFile(dataURL)
			// newFile.src = dataURL
			return dataURL
		})
	}
}