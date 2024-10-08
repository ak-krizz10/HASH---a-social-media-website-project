function handleLikeClick(postId, csrftoken) {
    let svg = document.getElementById(`heart${postId}`);
    let likeCountContainer = document.getElementById(`num${postId}`);
  
    let url = "{% url 'like' %}";
    const data = { id: postId };
  
    fetch(url, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
  
      if (data["check"]) {
        svg.innerHTML = `<path fill=var(--clr-rose) d="m480-120-58-52q-101-91-167-157T150-447.5Q111-500 95.5-544T80-634q0-94 63-157t157-63q52 0 99 22t81 62q34-40 81-62t99-22q94 0 157 63t63 157q0 46-15.5 90T810-447.5Q771-395 705-329T538-172l-58 52Z"/>`;
        svg.classList.add('like-animation');
      } else {
        svg.innerHTML = `<path fill=var(--clr-light) d="m480-146.925-44.153-39.691q-99.461-90.231-164.5-155.077-65.038-64.846-103.076-115.423-38.039-50.577-53.154-92.269-15.116-41.692-15.116-84.615 0-85.153 57.423-142.576Q214.847-833.999 300-833.999q52.385 0 99 24.501 46.615 24.5 81 70.269 34.385-45.769 81-70.269 46.615-24.501 99-24.501 85.153 0 142.576 57.423Q859.999-719.153 859.999-634q0 42.923-15.116 84.615-15.115 41.692-53.154 92.269-38.038 50.577-102.884 115.423T524.153-186.616L480-146.925ZM480-228q96-86.385 158-148.077 62-61.692 98-107.192 36-45.5 50-80.808 14-35.308 14-69.923 0-60-40-100t-100-40q-47.385 0-87.577 26.885-40.192 26.884-63.654 74.808h-57.538q-23.846-48.308-63.846-75.001Q347.385-774 300-774q-59.615 0-99.808 40Q160-694 160-634q0 34.615 14 69.923t50 80.808q36 45.5 98 107T480-228Zm0-273Z"/>`;
        svg.classList.remove('like-animation');
        svg.classList.add('scale-down-animation');
        setTimeout(() => {
          svg.classList.remove('scale-down-animation');
        }, 300);
      }
  
      likeCountContainer.innerText = data["num_of_likes"];
    });
  }
  