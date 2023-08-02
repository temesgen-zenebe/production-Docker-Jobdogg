window.addEventListener("DOMContentLoaded", (event) => {
    var cardTag = document.querySelectorAll(".job-card__tags li");
    var filterTagClose = document.querySelectorAll("#filter-tags-list li span");
  
    for (var i = 0; i < cardTag.length; i++) {
      cardTag[i].addEventListener("click", tagClicked(i));
    }
  
    for (var i = 0; i < filterTagClose.length; i++) {
      filterTagClose[i].addEventListener("click", closeClicked(i));
    }
  
    refreshList();
  
    //When a card tag is clicked
    function tagClicked(i) {
      //Get tag value
      var cardText = cardTag[i].innerHTML;
  
      //Create filter tag
      var newTag = document.createElement("li");
      newTag.innerHTML =
        "<p>" + cardText + '</p><span class="close-span">×</span>';
  
      return function () {
        //check if tag already exits
        var toAdd = true;
        var filterListing = document.querySelectorAll("#filter-tags-list li p");
        for (var keyValue = 0; keyValue < filterListing.length; keyValue++) {
          if (cardText == filterListing[keyValue].innerHTML) {
            toAdd = false;
          }
        }
  
        //Append filter tag to the list
        if (toAdd) {
          document.getElementById("filter-tags-list").appendChild(newTag);
        }
        refreshList();
      };
    }
  
    //When filter tag close is clicked
    function closeClicked(i) {
      return function () {
        filterTagClose[i].parentNode.remove();
        refreshList();
      };
    }
  
    //Clear all filter tags
    document
      .getElementById("js-clear-tags")
      .addEventListener("click", function () {
        document.getElementById("filter-tags-list").innerHTML = "";
        refreshList();
      });
  
    //Function to reload list of jobs
    function refreshList() {
      //Refresh the filter list
      filterTagClose = document.querySelectorAll("#filter-tags-list li span");
      var fiterC = document.getElementById("filter-tags-list").parentNode;
  
      for (var i = 0; i < filterTagClose.length; i++) {
        filterTagClose[i].addEventListener("click", closeClicked(i));
      }
  
      //List Sorting
      var jobListing = document.querySelectorAll("#job-list>li");
      var filterListing = document.querySelectorAll("#filter-tags-list li p");
      var matches = 0;
  
      for (var job = 0; job < jobListing.length; job++) {
        var skillSet = jobListing[job].querySelectorAll(".job-card__tags li");
        matches = 0;
  
        for (var keyValue = 0; keyValue < filterListing.length; keyValue++) {
          for (var skill = 0; skill < skillSet.length; skill++) {
            if (skillSet[skill].innerHTML == filterListing[keyValue].innerHTML) {
              matches += 1;
            }
          }
        }
        if (matches == filterListing.length) {
          jobListing[job].classList.remove("d-none");
        } else {
          jobListing[job].classList.add("d-none");
        }
      }
  
      //Check if tags are present
      if (document.querySelectorAll("#filter-tags-list li").length) {
        fiterC.classList.remove("d-none");
      } else {
        fiterC.classList.add("d-none");
        for (var i = 0; i < jobListing.length; i++) {
          jobListing[i].classList.remove("d-none");
        }
      }
    }
  });
  




//$(document).ready(function() {
//$('.search-box').focus();
//});

const wrapper = document.querySelector(".wrapper");
const header = document.querySelector(".header");

wrapper.addEventListener("scroll", (e) => {
 e.target.scrollTop > 30
  ? header.classList.add("header-shadow")
  : header.classList.remove("header-shadow");
});

const toggleButton = document.querySelector(".dark-light");

toggleButton.addEventListener("click", () => {
 document.body.classList.toggle("dark-mode");
});

const jobCards = document.querySelectorAll(".job-card");
const logo = document.querySelector(".logo");
const jobLogos = document.querySelector(".job-logos");
const jobDetailTitle = document.querySelector(
 ".job-explain-content .job-card-title"
);
const jobBg = document.querySelector(".job-bg");

jobCards.forEach((jobCard) => {
 jobCard.addEventListener("click", () => {
  const number = Math.floor(Math.random() * 10);
  const url = `https://unsplash.it/640/425?image=${number}`;
  jobBg.src = url;

  const logo = jobCard.querySelector("svg");
  const bg = logo.style.backgroundColor;
  console.log(bg);
  jobBg.style.background = bg;
  const title = jobCard.querySelector(".job-card-title");
  jobDetailTitle.textContent = title.textContent;
  jobLogos.innerHTML = logo.outerHTML;
  wrapper.classList.add("detail-page");
  wrapper.scrollTop = 0;
 });
});

logo.addEventListener("click", () => {
 wrapper.classList.remove("detail-page");
 wrapper.scrollTop = 0;
   jobBg.style.background = bg;
});