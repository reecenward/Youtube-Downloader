const form = document.querySelector("form");

form.addEventListener("submit", event => {
    event.preventDefault();

    const fname = form.elements.fname.value;
    fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ fname })
        })
        .then(res => {
            console.log(res.headers.get('content-type'));
            return res.arrayBuffer();
        })
        .then(data => {
            console.log(data);
            const link = document.createElement('a');
            link.href = URL.createObjectURL(new Blob([data]));
            link.download = 'download.mp4';
            document.body.appendChild(link);
            link.click();
        });

});