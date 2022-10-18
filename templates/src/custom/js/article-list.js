ratingAll()

function ratingAll() {
    document.querySelectorAll('.btn-like, .btn-dislike').forEach((e) => {
    e.addEventListener('click', createRating)
})
}

function createRating(event) {
    event.preventDefault()
    const rating = this;
    const ratingId = rating.getAttribute('data-id');
    const ratingAction = rating.getAttribute('data-action');
    const ratingSum =  document.querySelector(`button[data-rating='${ratingId}']`);
    fetch(`/articles/${ratingId}/${ratingAction}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
        },
    }).then((response) => response.json()).then((result) => {
                if (result['error']) {
                    console.log(result['error'])
                } else {
                    ratingSum.innerHTML = `${result['get_rating_sum']} <i class="fa-solid fa-hand-holding-heart"></i>`
                }
        })
}