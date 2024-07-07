<script>
export default {
  
}
</script>

<template>
  <router-view/>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-size: 18px;
}

html, body, #app, .profile {
  height: 100%;
  margin: 0;
  padding: 0;
}

a {
  text-decoration: none;
}

.form-errors {
  color: red;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  margin: 0 10px;
  text-decoration: none;
}

.com__btn {
    --bs-btn-color: #fff;
    --bs-btn-bg: orangered;
    --bs-btn-border-color: orangered;
    --bs-btn-hover-color: #fff;
    --bs-btn-hover-bg: rgb(240, 70, 8);
    --bs-btn-hover-border-color: rgb(240, 70, 8);
    --bs-btn-focus-shadow-rgb: 49, 132, 253;
    --bs-btn-active-color: #fff;
    --bs-btn-active-bg: orangered;
    --bs-btn-active-border-color: orangered;
    --bs-btn-active-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
    --bs-btn-disabled-color: #fff;
    --bs-btn-disabled-bg: orangered;
    --bs-btn-disabled-border-color: orangered;
    cursor: pointer;

}

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
  transition: width 0.3s, height 0.3s;
}

::-webkit-scrollbar-track {
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.online {
    color: green;
}

.offline {
    color: red;
}



</style>
