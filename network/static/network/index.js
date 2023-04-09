import{getCookie, editPostButton, updatePost, likeButton, likeUnlike, toggleLikes } from "./script.js"
document.addEventListener('DOMContentLoaded', function(){
    
    if(document.querySelector('#post-area')){
        postArea();
    }
    //document.querySelector('#post-area').addEventListener('keyup', postArea)
    document.querySelector('#post-form').addEventListener('submit', postMessage);
    /*document.querySelector('#author-link').addEventListener('click', ()=>{
        profilePage()
    });*/
    
    
     editPostButton()
     likeButton();  
     
})

function postArea(){
    //const txtArea = document.querySelector('#post-area');
    //const formTextArea = document.querySelector('#post-area')
    const postBtn = document.querySelector('#post-btn')
   // console.log(`${formTextArea} and ${postBtn}`)
    document.querySelector('#post-area').addEventListener ('keyup', ()=>{
        if(document.querySelector('#post-area').value === ""){
            postBtn.style.display = "none"
            postBtn.disabled = true;
         }else{
             postBtn.disabled= false;
             postBtn.style.display = "block"
         }
    })
        
    
}

function postMessage(e){
   e.preventDefault();
    let message = document.querySelector('#post-area');
   
    const csrftoken = getCookie('csrftoken');
    //Post a message with REST API
    fetch('/newPost', {
        method: 'POST',
        credentials: 'same-origin',
        
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            body: message.value
        })
    })
    .then(response => response.json())
    .then(res => {
        console.log(res.message)
    })
    document.querySelector('#post-area').value="";
    window.location.reload();
    //document.querySelector('#all-posts-div').location.reload();
}


