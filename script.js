// let content = document.getElementById('content').value;
// let title = document.getElementById('title').value;
// let rating = document.getElementById('rating').value;



// fetch("http://127.0.0.1:8000/createposts",{
//     method:'POST',
//     headers:{
//         'Content-Type':'application/json'
//     },
//     body:JSON.stringify({
//         title:title,
//         content:content,
//         rating:rating
//     })
// })
// .then(res=>{
//     return res.json()})
// .then(data=>console.log(data))


document.getElementById("postForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form data
    let content = document.getElementById('content').value;
    let title = document.getElementById('title').value;
    let rating = document.getElementById('rating').value;

    // Send data to backend using Fetch API
    fetch("http://127.0.0.1:8000/createposts", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            content: content,
            rating: rating
        })
    })
    .then(res => {
        return res.json();
    })
    .then(data => {
        console.log(data); // Log response from backend
    })
    .catch(error => {
        console.error('Error:', error); // Handle errors
    });
});
