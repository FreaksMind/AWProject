<template>
  <ul class="tree">
    <li>
      <span @click="toggle">
        <span v-if="node.children.length > 0">
          {{ node.expanded ? "▼" : "▶" }}
        </span>
        {{ node.label }}
      </span>
      <ul v-show="node.expanded">
        <TreeNode v-for="child in node.children" :key="child.label" :node="child" @fetch-children="$emit('fetch-children', child)" />
      </ul>
    </li>
  </ul>
</template>

<script>
export default {
  props: ["node"],
  methods: {
    toggle() {
      this.$emit("fetch-children", this.node);
    }
  }
};
</script>

<style scoped>
.tree {
  list-style-type: none;
  padding-left: 20px;
}
li {
  cursor: pointer;
  padding: 5px;
}
li:hover {
  background-color: transparent;
}
</style>