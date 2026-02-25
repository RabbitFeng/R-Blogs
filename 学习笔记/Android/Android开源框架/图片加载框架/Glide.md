

> [Glide github](https://github.com/bumptech/glide)

sample

```java
  Glide
    .with(myFragment)
    .load(url)
    .centerCrop()
    .placeholder(R.drawable.loading_spinner)
    .into(myImageView);
```

## 链式调用说起

**加载大图都做了哪些优化**

做一个完整的项目，包含RecyclerView， 大图加载

- 下采样

- 缩略图

