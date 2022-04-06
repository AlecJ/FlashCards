<script>
export default {
    props: {
        width: String,
        height: String,
    },
};

</script>

<template>
  <div id="card" :style="{'width': this.width || '200px', 'height': this.height || '120px'}">
    <slot />
  </div>
</template>

<style scoped>
#card {
  background: rgba(50, 50, 50, 0.15);
  border-radius: 15px;
  margin: 5px;

  display: grid;
  align-items: center;
  justify-items: center;
}
</style>
