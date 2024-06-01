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
  /* background-color: darkgrey; */
}

a {
  text-decoration: none;
}

/* .main {

  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  align-items: flex-start;
  height: 80vh;
  max-width: 700px;
  margin: 10vh auto;
  box-shadow: 0 0 10px rgba(255, 69, 0, 0.5); 
  border-radius: 20px; 
  padding: 20px;

} */

.form-errors {
  color: red;
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
</style>
