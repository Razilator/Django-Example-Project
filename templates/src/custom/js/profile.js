const subscribeBtn = document.querySelector('.btn-following')
const followerBox = document.querySelector('#followersBox')

subscribeBtn.addEventListener('click', subscribeUser)

function subscribeUser() {
    const subscribe = this;
    const subscribeProfileSlug = subscribe.getAttribute('data-slug');
    fetch(`/s/user/${subscribeProfileSlug}/follow/`, {
        method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
    }).then((response) => response.json()).then((result) => {
        if (subscribeBtn.classList.contains('btn-primary')) {
            subscribeBtn.classList.remove('btn-primary')
            subscribeBtn.classList.add('btn-danger')
        } else {
            subscribeBtn.classList.remove('btn-danger')
            subscribeBtn.classList.add('btn-primary')
        }
        if (result['error']) {
            subscribeBtn.innerText = `${result['error']}`
        } else {
            if (result['status']) {
                followerBox.innerHTML += `
                     <div class="col-md-2" id="user-slug-${result['following_slug']}">
                         <a href="${result['following_get_absolute_url']}">
                           <img src="${result['following_avatar']}" class="img-fluid rounded-1" alt="${result['following_slug']}"/>
                         </a>
                      </div>
                `
                subscribeBtn.innerHTML = `${result['message']}`
            }
            else {
                const currentSlugUser = document.querySelector(`#user-slug-${result['following_slug']}`)
                currentSlugUser.remove()
                subscribeBtn.innerHTML = `${result['message']}`
            }
        }
    })
}