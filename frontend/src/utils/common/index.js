import router from '@/router'

export const replaceUrl = ({query, params}) => {
    // type query and params is object
    // exp: {id: 1}
    router
        .replace({
            query: query,
            params: params
        })
        .catch((e) => {
            console.log(e)
        })
}

export const readFile = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = () => resolve(reader.result)
  })
}
