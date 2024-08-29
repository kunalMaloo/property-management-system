const wrapper = document.querySelector(".wrapper");
const loginLink = document.querySelector(".login-link");
const registerLink = document.querySelector(".register-link");
const btnPopup = document.querySelector(".btnLogin-popup");
const iconClose = document.querySelector(".icon-close");
const navbar = document.querySelector(".navbar");
const navbarElement = document.getElementById("navbar");
const navbarHeight = navbarElement.offsetHeight;
let position = null;

registerLink.addEventListener("click", () => {
  wrapper.className = "wrapper active active-popup";
});

loginLink.addEventListener("click", () => {
  wrapper.className = "wrapper active-popup";
});

if (btnPopup) {
  btnPopup.addEventListener("click", () => {
    const wrapperIsActive = wrapper.classList.contains("active");
    const wrapperIsPopupActive = wrapper.classList.contains("active-popup");
    const targetPosition =
      wrapperIsActive && !wrapperIsPopupActive
        ? navbar.getBoundingClientRect().top
        : position;

    window.scrollTo({
      top: targetPosition,
      behavior: "smooth",
    });

    wrapper.classList.toggle("active-popup");
    position = wrapperIsPopupActive ? position : window.scrollY;
  });
}

iconClose.addEventListener("click", () => {
  window.scrollTo({
    top: position,
    behavior: "smooth",
  });

  wrapper.classList.remove("active-popup");
});

window.addEventListener("scroll", () => {
  if (window.scrollY >= navbarHeight) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});
