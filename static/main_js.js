// 마우스 이벤트
// 마우스 올리기 - onmouseover, 마우스 내리기 - onmouseout
// addEvertListener() - mouseover, mouseout 사용(on생략)
let pic = document.getElementById('pic');
//pic.onmouseover = changePic;
//pic.onmouseout = originPic;

pic.addEventListener('mouseover',changePic)
pic.addEventListener('mouseout', originPic)



function changePic(){
    pic.src = "../static/coffee-blue.jpg";
}
function originPic(){
    pic.src = "../static/coffee-gray.jpg";
}

setInterval(function(){
        const now = new Date();
        let watch = now.toLocaleTimeString();
        document.querySelector("#display").innerHTML = watch;
     },1000)