document.addEventListener("DOMContentLoaded", () => {
    console.log("[Highlight JS] DOM fully loaded.");

    const anchors = document.querySelectorAll("a[href^='#__codelineno']");
    console.log(`[Highlight JS] Found ${anchors.length} line anchors.`);

    // Apply highlight on click
    anchors.forEach(anchor => {
        anchor.addEventListener("click", () => {
            highlightLine(anchor.getAttribute("href").substring(1));
        });
    });

    // Apply highlight on initial load if there's a line in the hash
    const initialHash = window.location.hash;
    if (initialHash.startsWith("#__codelineno")) {
        const id = initialHash.substring(1);
        highlightLine(id);
        console.log(`[Highlight JS] Initial highlight for: ${id}`);
    }
});

function highlightLine(id) {
    // Remove existing highlights
    document.querySelectorAll(".highlighted-line").forEach(el =>
        el.classList.remove("highlighted-line")
    );

    const targetTd = document.getElementById(id);
    if (targetTd && targetTd.parentElement) {
        targetTd.parentElement.classList.add("highlighted-line");
        console.log(`[Highlight JS] Added highlight to row of: #${id}`);
    } else {
        console.warn(`[Highlight JS] Could not find row for: ${id}`);
    }
}
