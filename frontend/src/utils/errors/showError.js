import { i18n } from '@/plugins'

export const showError = (
    e, toast, defaultMessage = i18n.t('master.msg.get_data_failed')
) => {
  if (e.response?.data?.detail) {
    const { detail } = e.response.data
    if (detail?.msg) toast.error(detail?.msg)
    else if (detail?.error_code) toast.error(i18n.t(`error_code.${detail?.error_code}`))
    else toast.error(detail)
  } else {
    toast.error(defaultMessage)
  }
}

export const scrollTop = () => {
  window.scrollTo(0, 0)
}

export const scrollBottom = () => {
  window.setTimeout(() => {
    window.scrollTo(0, document.body.scrollHeight)
  }, 300)
}
