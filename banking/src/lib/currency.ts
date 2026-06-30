export const getCurrencySymbol = (currency: string) => {
    // @ts-expect-error - Boot is available
    if (terminal_framework.boot) {
        // @ts-expect-error - Boot is available
        if (terminal_framework.boot.sysdefaults && terminal_framework.boot.sysdefaults.hide_currency_symbol == "Yes")
            return "";
        // @ts-expect-error - Boot is available
        if (!currency) currency = terminal_framework.boot.sysdefaults.currency;

        return getCurrencyProperty(currency, 'symbol') || currency;
    } else {
        return getCurrencyProperty(currency, 'symbol') || currency
    }
}

export const getCurrencyNumberFormat = (currency: string) => {
    return getCurrencyProperty(currency, 'number_format')
}


export const getCurrencyProperty = (currency: string, property: 'symbol' | 'symbol_on_right' | 'number_format') => {
    // @ts-expect-error - Locals is synced
    return locals[':Currency']?.[currency]?.[property]
}