export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function editPostButton(){
    document.querySelectorAll('#edit-button').forEach((post) =>{
        
        post.addEventListener('click', (e)=>{
            const editBtn = e.target;
            editBtn.style.display = 'none';
            const postBodyPTag = editBtn.parentElement.previousElementSibling;//The post body or content paragraph tag.
            postBodyPTag.style.display ="none";
            const editFormDiv = editBtn.parentElement.nextElementSibling//The div that contains the form..
            console.log(`nextSib = ${editFormDiv.className}`)
            editFormDiv.className = "body-data"
            editFormDiv.style.display= "block";
            let postBody= editBtn.dataset.post;
            const updateButton =document.querySelector('#update-button');
            updateButton.dataset.id = `${e.target.dataset.id}`;
            
            console.log(postBody)
            console.log(document.querySelector('#edit-e.target.dataset.id'))
            editFormDiv.querySelector('#edit-post-area').value=`${postBody}`
            
            console.log(editFormDiv.querySelector('#update-button'))
            const editForm = editFormDiv.querySelector('#post-form')
            console.log(editForm)
            editForm.querySelector('#update-button').addEventListener('click', (e)=>{
                e.preventDefault();
                const postID = e.target.dataset.id
                console.log(postID)
                const updatedPost = editFormDiv.querySelector('#edit-post-area').value;
                updatePost(postID, updatedPost, postBodyPTag, editFormDiv, editBtn)
             });
         });
    })
}

export function updatePost(postID, updatedPost, postBodyPTag, editFormDiv, editBtn){
    // const message =document.querySelector('#edit-post-area')
     console.log('inside edit post');
     const csrftoken = getCookie('csrftoken');
     //update a post with REST API PUT method,fetching data from dom
     fetch(`networks/${postID}/editPost`, {
         method: 'PUT',
         credentials: 'same-origin',
         
         headers: {
             'Content-Type': 'application/json',
             'X-Requested-With': 'XMLHttpRequest',
             'Accept': 'application/json',
             'X-CSRFToken': csrftoken},
         body: JSON.stringify({
             body: updatedPost
         })
     })
     .then(response => response.json())
     .then(res => {
         console.log(res.message)
         postBodyPTag.innerHTML =`${res.post.body}`
         editBtn.dataset.post = `${res.post.body}`
         
     })
     postBodyPTag.style.display = "block"
     editFormDiv.style.display= "none";
     editBtn.style.display = "block"
    }
 
 
 
export function likeButton(){
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
 
export function likeUnlike(postElement, likeCount){
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
 
export function toggleLikes(postID, postElement){
     let postId = parseInt(postID)
     console.log(postId)
     fetch(`networks/${postId}/likePost`)
     .then(response => response.json())
     .then(res => {
         likeUnlike(postElement, res.post.likes.length)
     })
     console.log('Just done with fetch inside toggle function');
 }
 
 