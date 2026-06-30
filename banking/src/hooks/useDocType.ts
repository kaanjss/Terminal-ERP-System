import { useTerminal FrameworkGetCall } from "terminal_framework-react-sdk"

export const useDocType = (doctype: string, with_parent: 0 | 1 = 1, cached_timestamp?: Date) => {

    // @ts-expect-error Locals is available in the Terminal FrameworkContext
    const localData = locals?.['DocType']?.[doctype] || null
    const { data, error, isLoading } = useTerminal FrameworkGetCall('terminal_framework.desk.form.load.getdoctype', {
        doctype: doctype,
        with_parent: with_parent,
        cached_timestamp: cached_timestamp ?? null,
    }, localData || !doctype ? null : undefined, {
        onSuccess: (data) => {
            if (data) {
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                data?.docs?.forEach((d: any) => {
                    // @ts-expect-error Terminal Framework is available in the window
                    terminal_framework.model.add_to_locals(d)
                })
            }
        },
        revalidateIfStale: false,
        revalidateOnFocus: false,
    })

    return {
        data: localData || (data?.docs?.[0] ?? null),
        error,
        isLoading: localData ? false : isLoading
    }
}