Comparing经常用，但是今天发现了几个新的用法，比如倒序可以直接用.reversed()，话不多说，直接上代码：

```java
public class CompareTest {
    public static void main(String[] args) {

        List<Employee> employeeList = new ArrayList<>();
        employeeList.add(new Employee("a", 18));
        employeeList.add(new Employee("b", 15));
        employeeList.add(new Employee("c", 20));

        // 匿名内部类
        employeeList.sort(new Comparator<Employee>() {
            @Override
            public int compare(Employee e1, Employee e2) {
                return e1.getAge().compareTo(e2.getAge());
            }
        });
        // lambda表达式
        employeeList.sort((e1, e2) -> e1.getAge().compareTo(e2.getAge()));
        // 静态方法comparing
        employeeList.sort(Comparator.comparing(Employee::getAge));
        // 倒序
        employeeList.sort(Comparator.comparing(Employee::getAge).reversed());
        // thenComparing
        employeeList.sort(Comparator.comparing(Employee::getAge).reversed().thenComparing(Employee::getName));
    }
    
    @Data
    @AllArgsConstructor
    static class Employee {

        private String name;

        private Integer age;
    }
}
```