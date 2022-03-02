function checkWriting(){
    let form = document.writeForm;
    let title = form.title.value;
    let content = form.content.value;

    if(title == ""){
        alert("제목은 필수 항목입니다.");
        form.title.focus();
        return false;
    }
    else if(content == ""){
        alert("내용은 필수 항목입니다.");
        form.content.focus();
        return false;
    }
    else{
        form.submit();
    }
}