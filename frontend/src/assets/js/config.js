let isProduction = process.env.NODE_ENV === 'production'
const BASE_URL = '/'
export default {
	baseUrl: BASE_URL,
	baseApi: isProduction ? BASE_URL : '/api/',
}