document.addEventListener('DOMContentLoaded', function(){
    likeButton();  
      
      
})

function likeButton(){
    const likeBtn = document.querySelectorAll('.like-italic')
    likeBtn.forEach((like) =>{
        like.addEventListener('click', (e)=>{
            //copy below code and create a new function out of it.
            const postElement = e.target;
            const postID = e.target.dataset.id
            console.log(like)
            console.log(e.target.nextSibling)
            //likeUnlike(e.target);
            toggleLikes(postID, postElement);
            console.log(e.target.dataset.id)
        })
    })
}

function likeUnlike(postElement, likeCount){
    let countLike = likeCount;
    if(postElement.classList.contains('far')){
        postElement.classList.remove('far')
        postElement.classList.add('fas');
        postElement.nextElementSibling.innerHTML = `${countLike}`
        postElement.nextElementSibling.className ="added-likes"
    }else{
        postElement.classList.remove('fas')
        postElement.classList.add('far')
       // countLike--
        postElement.nextElementSibling.innerHTML = `${countLike}`
        postElement.nextElementSibling.className ="unlike"
    }
}

function toggleLikes(postID, postElement){
    let postId = parseInt(postID)
    console.log(postId)
    fetch(`${postId}/likePost`)
    .then(response => response.json())
    .then(res => {
        likeUnlike(postElement, res.post.likes.length)
    })
    console.log('Just done with fetch inside toggle function');
}