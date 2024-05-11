## Q&A

### 1. `getMethod()` 和 `getDeclaredMehod()`方法的区别

[Class.java JDK 8](https://docs.oracle.com/javase/8/docs/api/java/lang/Class.html)

```java
    /**
     * Returns a {@code Method} object that reflects the specified public
     * member method of the class or interface represented by this
     * {@code Class} object. The {@code name} parameter is a
     * {@code String} specifying the simple name of the desired method. The
     * {@code parameterTypes} parameter is an array of {@code Class}
     * objects that identify the method's formal parameter types, in declared
     * order. If {@code parameterTypes} is {@code null}, it is
     * treated as if it were an empty array.
     *
     * <p> If the {@code name} is "{@code <init>}" or "{@code <clinit>}" a
     * {@code NoSuchMethodException} is raised. Otherwise, the method to
     * be reflected is determined by the algorithm that follows.  Let C be the
     * class or interface represented by this object:
     * <OL>
     * <LI> C is searched for a <I>matching method</I>, as defined below. If a
     *      matching method is found, it is reflected.</LI>
     * <LI> If no matching method is found by step 1 then:
     *   <OL TYPE="a">
     *   <LI> If C is a class other than {@code Object}, then this algorithm is
     *        invoked recursively on the superclass of C.</LI>
     *   <LI> If C is the class {@code Object}, or if C is an interface, then
     *        the superinterfaces of C (if any) are searched for a matching
     *        method. If any such method is found, it is reflected.</LI>
     *   </OL></LI>
     * </OL>
     *
     * <p> To find a matching method in a class or interface C:&nbsp; If C
     * declares exactly one public method with the specified name and exactly
     * the same formal parameter types, that is the method reflected. If more
     * than one such method is found in C, and one of these methods has a
     * return type that is more specific than any of the others, that method is
     * reflected; otherwise one of the methods is chosen arbitrarily.
     *
     * <p>Note that there may be more than one matching method in a
     * class because while the Java language forbids a class to
     * declare multiple methods with the same signature but different
     * return types, the Java virtual machine does not.  This
     * increased flexibility in the virtual machine can be used to
     * implement various language features.  For example, covariant
     * returns can be implemented with {@linkplain
     * java.lang.reflect.Method#isBridge bridge methods}; the bridge
     * method and the method being overridden would have the same
     * signature but different return types.
     *
     * <p> If this {@code Class} object represents an array type, then this
     * method does not find the {@code clone()} method.
     *
     * <p> Static methods declared in superinterfaces of the class or interface
     * represented by this {@code Class} object are not considered members of
     * the class or interface.
     *
     * @param name the name of the method
     * @param parameterTypes the list of parameters
     * @return the {@code Method} object that matches the specified
     *         {@code name} and {@code parameterTypes}
     * @throws NoSuchMethodException if a matching method is not found
     *         or if the name is "&lt;init&gt;"or "&lt;clinit&gt;".
     * @throws NullPointerException if {@code name} is {@code null}
     * @throws SecurityException
     *         If a security manager, <i>s</i>, is present and
     *         the caller's class loader is not the same as or an
     *         ancestor of the class loader for the current class and
     *         invocation of {@link SecurityManager#checkPackageAccess
     *         s.checkPackageAccess()} denies access to the package
     *         of this class.
     *
     * @jls 8.2 Class Members
     * @jls 8.4 Method Declarations
     * @since JDK1.1
     */
    @CallerSensitive
    public Method getMethod(String name, Class<?>... parameterTypes)
        throws NoSuchMethodException, SecurityException {
        checkMemberAccess(Member.PUBLIC, Reflection.getCallerClass(), true);
        Method method = getMethod0(name, parameterTypes, true);
        if (method == null) {
            throw new NoSuchMethodException(getName() + "." + name + argumentTypesToString(parameterTypes));
        }
        return method;
    }

    /**
     * Returns a {@code Method} object that reflects the specified
     * declared method of the class or interface represented by this
     * {@code Class} object. The {@code name} parameter is a
     * {@code String} that specifies the simple name of the desired
     * method, and the {@code parameterTypes} parameter is an array of
     * {@code Class} objects that identify the method's formal parameter
     * types, in declared order.  If more than one method with the same
     * parameter types is declared in a class, and one of these methods has a
     * return type that is more specific than any of the others, that method is
     * returned; otherwise one of the methods is chosen arbitrarily.  If the
     * name is "&lt;init&gt;"or "&lt;clinit&gt;" a {@code NoSuchMethodException}
     * is raised.
     *
     * <p> If this {@code Class} object represents an array type, then this
     * method does not find the {@code clone()} method.
     *
     * @param name the name of the method
     * @param parameterTypes the parameter array
     * @return  the {@code Method} object for the method of this class
     *          matching the specified name and parameters
     * @throws  NoSuchMethodException if a matching method is not found.
     * @throws  NullPointerException if {@code name} is {@code null}
     * @throws  SecurityException
     *          If a security manager, <i>s</i>, is present and any of the
     *          following conditions is met:
     *
     *          <ul>
     *
     *          <li> the caller's class loader is not the same as the
     *          class loader of this class and invocation of
     *          {@link SecurityManager#checkPermission
     *          s.checkPermission} method with
     *          {@code RuntimePermission("accessDeclaredMembers")}
     *          denies access to the declared method
     *
     *          <li> the caller's class loader is not the same as or an
     *          ancestor of the class loader for the current class and
     *          invocation of {@link SecurityManager#checkPackageAccess
     *          s.checkPackageAccess()} denies access to the package
     *          of this class
     *
     *          </ul>
     *
     * @jls 8.2 Class Members
     * @jls 8.4 Method Declarations
     * @since JDK1.1
     */
    @CallerSensitive
    public Method getDeclaredMethod(String name, Class<?>... parameterTypes)
        throws NoSuchMethodException, SecurityException {
        checkMemberAccess(Member.DECLARED, Reflection.getCallerClass(), true);
        Method method = searchMethods(privateGetDeclaredMethods(false), name, parameterTypes);
        if (method == null) {
            throw new NoSuchMethodException(getName() + "." + name + argumentTypesToString(parameterTypes));
        }
        return method;
    }
```

`getDeclaredMethods` includes all methods declared *by the class itself*, whereas `getMethods` returns only public methods, but also those inherited from a base class (here from `java.lang.Object`).

> `getDeclaredMethods` 包括**类本身声明的所有方法**，而 `getMethods` 只返回公共方法，但也返回从基类（此处来自 `java.lang.Object`）继承的方法。

21



## Short Version

| Method                 | Public | Non-public | Inherited |
| ---------------------- | ------ | ---------- | --------- |
| `getMethods()`         | ✔️      | ❌          | ✔️         |
| `getDeclaredMethods()` | ✔️      | ✔️          | ❌         |

## Long version

| Methods                     | getMethods() | getDeclaredMethods |
| --------------------------- | ------------ | ------------------ |
| public                      | ✔️            | ✔️                  |
| protected                   | ❌            | ✔️                  |
| private                     | ❌            | ✔️                  |
| static public               | ✔️            | ✔️                  |
| static protected            | ❌            | ✔️                  |
| static private              | ❌            | ✔️                  |
| default public              | ✔️            | ✔️                  |
| default protected           | ❌            | ✔️                  |
| default private             | ❌            | ✔️                  |
| inherited public            | ✔️            | ❌                  |
| inherited protected         | ❌            | ❌                  |
| inherited private           | ❌            | ❌                  |
| inherited static private    | ✔️            | ❌                  |
| inherited static protected  | ❌            | ❌                  |
| inherited static private    | ❌            | ❌                  |
| default inherited public    | ✔️            | ❌                  |
| default inherited protected | ❌            | ❌                  |
| default inherited private   | ❌            | ❌                  |

If your goal, like mine, was to get **public** methods of a class:

| Method                 | Public | Non-public | Inherited |
| ---------------------- | ------ | ---------- | --------- |
| `getMethods()`         | ✔️      | ❌          | ✔️         |
| `getDeclaredMethods()` | ✔️      | ✔️          | ❌         |
| getPublicMethods()     | ✔️      | ❌          | ❌         |

and nothing else:

| Methods                     | getPublicMethods() |
| --------------------------- | ------------------ |
| public                      | ✔️                  |
| protected                   | ❌                  |
| private                     | ❌                  |
| static public               | ❌                  |
| static protected            | ❌                  |
| static private              | ❌                  |
| default public              | ❌                  |
| default protected           | ❌                  |
| default private             | ❌                  |
| inherited public            | ❌                  |
| inherited protected         | ❌                  |
| inherited private           | ❌                  |
| inherited static private    | ❌                  |
| inherited static protected  | ❌                  |
| inherited static private    | ❌                  |
| default inherited public    | ❌                  |
| default inherited protected | ❌                  |
| default inherited private   | ❌                  |

### 2. 静态方法怎么调用

静态方法不属于类的实例方法，在使用`method.invoke()`方法调用时，参数传`null` 即可

### 3. 反射流程及原理

### 4. 注解

