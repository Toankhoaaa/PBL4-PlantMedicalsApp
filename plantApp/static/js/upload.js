const dropArea = document.querySelector(".drag-area"),
  dragText = dropArea.querySelector("header"),
  button = dropArea.querySelector("button"),
  input = dropArea.querySelector("input");
let file; // this is a global variable and we'll use it inside multiple functions

button.onclick = () => {
  input.click(); // if user clicks the button, then the input also gets clicked
};

input.addEventListener("change", function() {
  // getting the user-selected file and [0] means if user selects multiple files, we select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); // calling function to display the file
});

// If user drags a file over the DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault(); // preventing the default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

// If user leaves the dragged file from the DropArea
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

// If user drops a file on the DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault(); // preventing the default behaviour
  // getting the user-selected file and [0] means if user selects multiple files, we select only the first one
  file = event.dataTransfer.files[0];
  showFile(); // calling function to display the file
});

function showFile() {
  let fileType = file.type; // getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; // valid image extensions
  if (validExtensions.includes(fileType)) { // if the user selected an image file
    let fileReader = new FileReader(); // creating new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result; // storing the user file source in fileURL
      let imgTag = `<img src="${fileURL}" alt="image">`; // creating an img tag with the user-selected file as the source
      dropArea.innerHTML = imgTag; // adding the img tag inside the dropArea container
    };
    fileReader.readAsDataURL(file); // reading the file as a data URL
  } else {
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}
