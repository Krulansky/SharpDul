// Browser helpers called from C# through IJSRuntime.
window.sharpDul = {
    // On iPhone the share sheet offers "Save to Files"; elsewhere the file is downloaded.
    saveTextFile: async function (fileName, text) {
        const file = new File([text], fileName, { type: "application/json" });

        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            try {
                await navigator.share({ files: [file] });
                return;
            } catch (e) {
                if (e.name === "AbortError") {
                    return;
                }
            }
        }

        const url = URL.createObjectURL(file);
        const link = document.createElement("a");
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
    }
};
