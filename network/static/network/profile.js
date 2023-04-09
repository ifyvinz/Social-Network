import{getCookie, editPostButton, updatePost, likeButton, likeUnlike, toggleLikes } from "./script.js"
document.addEventListener('DOMContentLoaded', function(){
  editPostButton()
  likeButton();  
    const followButton = document.querySelector('#follow-button');
    if(followButton){
        followButton.addEventListener('click',(e)=>{
            console.log(e.target.dataset.user)
            const userName = e.target.dataset.user;
            console.log(userName)
            toggleFollow(userName)
        } )
    }

  if( document.querySelector('#Edit-profile-button')){
    document.querySelector('#Edit-profile-button').addEventListener('click', ()=>{
      console.log("YEs i am ready to edited")
          document.querySelector('#all-posts-div').style.display = "none";
          document.querySelector('#profile-form-div').style.display = "block";
    })
  }
 

  document.querySelector('#profile-button').addEventListener('click', editProfile);

    
    
})

function toggleFollow(userName){
  //const csrftoken = getCookie('csrftoken');
    fetch(`${userName}/connection`)
    .then(response => response.json())
    .then(res => {
         const following = document.querySelector('#following-count');
         following.innerHTML = "";
         console.log(document.querySelector('#followers-count'))
         const follower = document.querySelector('#followers-count');
         follower.innerHTML = "";
         const followButton = document.querySelector('#follow-button');
         
         following.innerHTML =`${res.following}`;
         follower.innerHTML = `${res.followers}`;
         followButton.textContent = `${res.related}`;
    })
  
    console.log("Toggled. Done..")
}

function editProfile(e){
    e.preventDefault();
   console.log("Yes editedPROFILE")
    //fields = ['id', 'user', 'name', 'about', 'country', 'photo']
    const userName = document.querySelector('#full-name').dataset.user
    const fullName = document.querySelector('#full-name').value;
    //const userName = fullName.dataset.user;
    const aboutMe = document.querySelector('#about-me').value;
    const country = document.querySelector('#country').value;
    const image = document.querySelector('#img')

    let formData = new FormData()
    formData.append('name', fullName);
    formData.append('about', aboutMe);
    formData.append('country', country);
    formData.append('image', image.files[0])
    const csrftoken = getCookie('csrftoken');
    fetch(`${userName}/editProfile`, {
        method: 'POST',
        credentials: 'same-origin',
        
        headers: {
            
            'X-CSRFToken': csrftoken},
        body : formData

    })
    .then(response => response.json())
    .then( data => {
         console.log(`Yes profile data: ${data.profile.country }of ${data.profile.name} ${data.profile.photo}`)
       
        document.querySelector('#all-posts-div').style.display = "block";
        document.querySelector('#profile-form-div').style.display = "none";
        console.log(document.querySelector('#profile-image'))
        
    })
      window.location.reload()
 
}
