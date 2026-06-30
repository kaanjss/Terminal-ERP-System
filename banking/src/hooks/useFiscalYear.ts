import { useTerminal FrameworkGetCall } from "terminal_framework-react-sdk"

const useFiscalYear = () => {

    return useTerminal FrameworkGetCall("terminal_erp.accounts.utils.get_fiscal_year", undefined, 'fiscal_year', {
        revalidateOnFocus: false,
        revalidateIfStale: false,
        revalidateOnReconnect: false
    })

}

export default useFiscalYear