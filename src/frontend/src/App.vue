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

a {
  text-decoration: none;
}

.main {

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

}

.form-errors {
  color: red;
}
</style>
