Java虚拟机的指令由一**个字节长度**的、**代表着某种特定操作含义的数字**（称为**操作码**，Opcode）以及跟随其后的零至多个代表此操作所需参数（称为**操作数**，Operands）而构成。由于**Java虚拟机采用面向操作数栈**而不是寄存器的架构，所以**大多数的指令都不包含操作数，只有一个操作码**。



## 加载和存储指令

加载和存储指令用于将数据从栈帧的本地变量表和操作数栈之间来回传递：

将一个本地变量加载到操作数栈的指令：：iload、iload_＜n＞、lload、lload_＜n＞、fload、fload_＜n＞、dload、dload_＜n＞、aload、aload_＜n＞。这里load后面的<n>代表的是当前栈帧中局部变量表的索引值，执行load操作后会把位于索引n位置的数据入栈到操作数栈顶。
将一个数值从操作数栈存储到局部变量表的指令：istore、istore_＜n＞、lstore、lstore_＜n＞、fstore、fstore_＜n＞、dstore、dstore_＜n＞、astore、astore_＜n＞。这里store后面的<n>代表的是当前栈帧中局部变量表的索引值，执行store操作后会把操作数栈顶的数据出栈，然后保存到位于索引n位置的局部变量表中。
将一个常量加载到操作数栈的指令：bipush、sipush、ldc、ldc_w、ldc2_w、aconst_null、iconst_m1、iconst_＜i＞、lconst_＜l＞、fconst_＜f＞、dconst_＜d＞。const操作就是把对应类型的常量数据入栈到操作数栈的栈顶。例如iconst_10则表示把int类型的常量10入栈到操作数栈顶。
扩充局部变量表的访问索引的指令：wide
我们看到上面有很多指令都是 指令_<n>，比如iload_<n>其实是表示一组指令（iload_<0>，iload_<1>，iload_<2>，iload_<3>）。在尖括号之间的字面指定了隐含操作数的数据类型：<n>代表的是非负的整数，<i>代表的是int类型数据，<l>代表long类型，<f>代表float类型，<d>代表double类型。操作byte，char和short类型的数据时，经常用int类型的指令来表示。

如果是实例方法（非static的方法），那么局部变量表中第0位索引的Slot默认是用于传递方法所属对象实例的引用"this"。其余参数则按照参数表的顺序来排列，占用从1开始的局部变量Slot，参数表分配完毕后，再根据方法体内部定义的变量顺序和作用域分配其余的Slot（比如方法method(int a1,inta2)，参数表为a1和a2，则局部变量表索引0、1、2则分别存储了this指针、a1、a2，如果方法内部有其他内部变量，则在局部变量表中存在a2之后的位置）。 

## 算术指令

算术指令用于对两个操作数栈上的值进行某种特定运算，并把结果重新压入操作数栈。大体上算术指令可以分为两种：对整型数据进行运算的指令与对浮点类型数据进行运算的指令。在每一大类中，都有针对Java虚拟机具体数据类型的专用算术指令。但没有直接支持byte、short、char和boolean类型的算术指令。对于这些数据的运算，都使用int类型的衍令来处理：整型与浮点类型的算术指令在溢出和被零除的时候也有各自不同的行为表现。

Java虚拟机的指令集直接支持了在Java语言规范中描述的各种对整型及浮点类型数进行操作的语义。Java虚拟机没有明确规定整型数据溢出（两个很大的整数相加，可能出现的结果是负数）的情况，只有整数除法指令（idiv和Idiv）及整数求余指令（irem和lrem）在除数为零时会导致虚拟机抛出异常。如果发生了这种情况，虚拟机将会抛出ArlthmeticException异常。

虚拟机要求在进行浮点数运算时，所有的运算结果都必须舍入到适当的梢度。非精确的结果必须舍入为可表示的最接近的精确值，如果有两种可表示的形式与该值一样接近，那将有些选择最低有效位为0的。这种舍入方式称为向最接近数舍入模式。

## 类型转换指令

类型转换指令可以将两种不同的数值类型进行相互转换。这些转换操作一般用于实现用户代码中的显式类型转换操作，或者用来处理字节码指令的不完备的问题（上面说的byte、short、char和boolean）。

Java虚拟机支持宽化类型转换（小范围类型向大范围类型的转换）、窄化类型转换（大范围类型向小范围类型的转换）两种：

宽化类型转换

int类型到long、float或者double类型。
long类型到float、double类型。
float类型到double类型。
类型转换指令有：i2l、i2f，i2d、l2f、l2d、f2d。"2"表示to的意思，比如i2l表示int转换成long。宽化类型转换是不会导致Java虚拟机抛出运行时异常的。

窄化类型转换：

从int类型到byte、short或者char类型

从long类型到int类型

从float类型到int或者long类型

从double类型到int、long或者float类型

窄化类型转换指令包括i2b、i2c、i2s、l2i、f2i、f2l、d2i、d2l和d2f。窄化类型转换可能会导致转换结果具备不同的正负号、不同的数量级，因此，转换过程很可能会导致数值丢失精度。窄化类型转换是不会导致Java虚拟机抛出运行时异常的。

## 对象创建与访问指令

虽然类实例和数组都是对象，但Java虚拟机对类实例和数组的创建与操作使用了不同的字节码指令。对象创建后，就可以通过对象访问指令获取对象实例或者数组实例中的字段或者数组元素。

## 操作数栈管理指令

Java虚拟机提供了一些用于直接控制操作数栈的指令，包括：pop，pop2，dup，dup2，dup_x1，dup2_x1，dup_x2，dup2_x2，swap。

## 控制转移指令

控制转移指令可以让Java虚拟机有条件或无条件地从指定的位置指令而不是控制转移指令的下一条指令继续执行程序。从概念模型上理解，可以认为控制转移指令就是在有条件或无条件地修改PC寄存器的值。

在Java虚拟机中有专门的指令集用来处理int和reference类型的条件分支比较操作，为了可以无须明显标识一个实体值是否null，也有专门的指令用来检测null值。

boolean、byte、char和short类型的条件分支比较操作，都使用int类型的比较指令来完成，而对于long、float和double类型的条件分支比较操作，则会先执行相应类型的比较运算指令，运算指令会返回一个整型数值到操作数栈中，随后再执行int类型的条件分支比较操作来完成整个分支跳转。由于各种类型的比较最终都会转化为int类型的比较操作，所以基于int类型比较的重要性，Java虚拟机提供了非常丰富的int类型的条件分支指令。

所有int类型的条件分支转移指令进行的都是有符号的比较操作。

## 方法调用和返回指令

invokevirtual 指令用于调用对象的实例方法，根据对象的实际类型进行分派（虚方法分派），这也是Java语言中最常见的方法分派方式。
invokeinterface 指令用于调用接口方法，它会在运行时搜索一个实现了这个接口方法的对象，找出适合的方法进行调用。
invokespecial 指令用于调用一些需要特殊处理的实例方法，包括实例初始化（＜init＞）方法、私有方法和父类方法。
invokestatic  调用静态方法（static方法）。
invokedynamic 指令用于在运行时动态解析出调用点限定符所引用的方法，并执行该方法，前面4条调用指令的分派逻辑都固化在Java虚拟机内部，而invokedynamic指令的分派逻辑是由用户所设定的引导方法决定的。
方法调用指令与数据类型无关，而方法返回指令是根据返回值的类型区分的，包括ireturn（当返回值是boolean、byte、char、short和int类型时使用）、lreturn、freturn、dreturn和areturn，另外还有一条return指令供声明为void的方法、实例初始化方法以及类和接口的类初始化方法使用。

## 异常处理指令

在Java程序中显式抛出异常的操作(throw语句）都由athrow指令来实现，除了用throw语句显式抛出异常情况之外，Java虚拟机规范还规定了许多运行时异常会在其他Java虚拟机指令检测到异常状况时自动抛出。例如，在前面介绍的整数运算中，当除数为零时，虚拟机会在idiv或Idiv指令中抛出ArithmeticExceptton异常。

而在Java虚拟机中，处理异常(catch语句）不是由字节码指令来实现的（很久之前曾经使用jsr和ret指令来实现，现在已经不用了），而是采用异常表来完成的。

## 同步指令

Java虚拟机可以支持方法级的同步和方法内部一段指令序列的同步，这两种同步结构都是使用同步锁（monitor）来支持的。

方法级的同步是隐式的，即无须通过字节码指令来控制，它实现在方法调用和返回操作之中。虚拟机可以从方法常量池的方法表结构中的ACC_SYNCHRONIZED访问标志得知一个方法是否声明为同步方法，当方法调用时，调用指令将会检查方法的ACC_SYNCHRONIZED访问标志是否被设置，如果设置了，执行线程就要求先成功持有同步锁，然后才能执行方法，最后当方法完成（无论是正常完成还是非正常完成）时释放同步锁。在方法执行期间，执行线程持有了同步锁，其他任何线程都无法再获取到同一个锁。如果一个同步方法执行期间抛出了异常，并且在方法内部无法处理此异常，那么这个同步方法所持有的锁将在异常抛到同步方法之外时自动释放。

同步一段指令集序列通常是由Java语言中的synchronized语句块来表示的，Java虚拟机的指令集中有monitorenter和monitorexit两条指令来支持synchronized关键字的语义，正确实现synchromzed关键字需要Javac编译器与Java虚拟两者共同协作支持。

package com.wkp.clone;

public class TestLock {

	public void onlyMe(Object f) {
		synchronized (f) {
			doSomething();
		}
	}
	 
	private void doSomething() {
		System.out.println("执行方法");
	}
}
上面代码通过 javap -c TestLock.class > TestLock.txt 将class文件进行反汇编，得到如下指令代码

Compiled from "TestLock.java"
public class com.wkp.clone.TestLock {
  public com.wkp.clone.TestLock();
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return

  public void onlyMe(java.lang.Object);
    Code:
       0: aload_1				//将对象f推送至操作数栈顶
       1: dup					//复制栈顶元素（对象f的引用）
       2: astore_2				//将栈顶元素复制到本地变量表Slot 2（第三个变量）
       3: monitorenter			//以栈顶元素对象f作为锁，开始同步
       4: aload_0				//将局部变量Slot 0(this指针)的元素入栈
       5: invokespecial #16     //调用doSomething()方法
       8: aload_2				//将本地变量表Slot 2元素（f）入栈
       9: monitorexit			//释放锁退出同步
      10: goto          16		//方法正常返回，跳转到16
      13: aload_2				//将本地变量表Slot 2元素（f）入栈
      14: monitorexit			//退出同步
      15: athrow				//将栈顶的异常对象抛给onlyMe的调用者
      16: return				//方法返回
    Exception table:
       from    to  target type
           4    10    13   any
          13    15    13   any
}
编译器必须确保无论方法通过何种方式完成，方法中调用过的每条momtor指令都必须执行其对应的momtorexlt指令，而无论这个方法是正常结東还是异常结束。

从上面的指令代码中可以看到，为了保证在方法异常完成时monitorenter和monitorexit指令依然可以正确配对执行，编译器会自动产生一个异常处理器，这个异常处理器声明可处理所有的异常，它的目的就是用来执行momtorexit指令。

————————————————
版权声明：本文为CSDN博主「没头脑遇到不高兴」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u012988901/article/details/99852568

| 指令码 | 助记符 | 说明 |
| ---- | ---- | ---- |
|  0x00  |  nop  |  无操作  |
|  0x01  |  aconst_null  |  将null推送至栈顶  |
|  0x02  |  iconst_m1  |  将int型-1推送至栈顶  |
|  0x03  |  iconst_0  |  将int型0推送至栈顶  |
|  0x04  |  iconst_1  |  将int型1推送至栈顶  |
|  0x05  |  iconst_2  |  将int型2推送至栈顶  |
|  0x06  |  iconst_3  |  将int型3推送至栈顶  |
|  0x07  |  iconst_4  |  将int型4推送至栈顶  |
|  0x08  |  iconst_5  |  将int型5推送至栈顶  |
|  0x09  |  lconst_0  |  将long型0推送至栈顶  |
|  0x0a  |  lconst_1  |  将long型1推送至栈顶  |
|  0x0b  |  fconst_0  |  将float型0推送至栈顶  |
|  0x0c  |  fconst_1  |  将float型1推送至栈顶  |
|  0x0d  |  fconst_2  |  将float型2推送至栈顶  |
|  0x0e  |  dconst_0  |  将double型0推送至栈顶  |
|  0x0f  |  dconst_1  |  将double型1推送至栈顶  |
|  0x10  |  bipush  |  将单字节的常量值(-128~127)推送至栈顶  |
|  0x11  |  sipush  |  将一个短整型常量值(-32768~32767)推送至栈顶  |
|  0x12  |  ldc  | 将int, float或String型常量值从常量池中推送至栈顶             |
|  0x13  |  ldc_w  | 将int, float或String型常量值从常量池中推送至栈顶（宽索引）   |
|  0x14  |  ldc2_w  |  将long或double型常量值从常量池中推送至栈顶（宽索引）  |
|  0x15  |  iload  |  将指定的int型本地变量推送至栈顶  |
|  0x16  |  lload  |  将指定的long型本地变量推送至栈顶  |
|  0x17  |  fload  |  将指定的float型本地变量推送至栈顶  |
|  0x18  |  dload  |  将指定的double型本地变量推送至栈顶  |
|  0x19  |  aload  |  将指定的引用类型本地变量推送至栈顶  |
|  0x1a  |  iload_0  |  将第一个int型本地变量推送至栈顶  |
|  0x1b  |  iload_1  |  将第二个int型本地变量推送至栈顶  |
|  0x1c  |  iload_2  |  将第三个int型本地变量推送至栈顶  |
|  0x1d  |  iload_3  |  将第四个int型本地变量推送至栈顶  |
|  0x1e  |  lload_0  |  将第一个long型本地变量推送至栈顶  |
|  0x1f  |  lload_1  |  将第二个long型本地变量推送至栈顶  |
|  0x20  |  lload_2  |  将第三个long型本地变量推送至栈顶  |
|  0x21  |  lload_3  |  将第四个long型本地变量推送至栈顶  |
|  0x22  |  fload_0  |  将第一个float型本地变量推送至栈顶  |
|  0x23  |  fload_1  |  将第二个float型本地变量推送至栈顶  |
|  0x24  |  fload_2  |  将第三个float型本地变量推送至栈顶  |
|  0x25  |  fload_3  |  将第四个float型本地变量推送至栈顶  |
|  0x26  |  dload_0  |  将第一个double型本地变量推送至栈顶  |
|  0x27  |  dload_1  |  将第二个double型本地变量推送至栈顶  |
|  0x28  |  dload_2  |  将第三个double型本地变量推送至栈顶  |
|  0x29  |  dload_3  |  将第四个double型本地变量推送至栈顶  |
|  0x2a  |  aload_0  |  将第一个引用类型本地变量推送至栈顶  |
|  0x2b  |  aload_1  |  将第二个引用类型本地变量推送至栈顶  |
|  0x2c  |  aload_2  |  将第三个引用类型本地变量推送至栈顶  |
|  0x2d  |  aload_3  |  将第四个引用类型本地变量推送至栈顶  |
|  0x2e  |  iaload  |  将int型数组指定索引的值推送至栈顶  |
|  0x2f  |  laload  |  将long型数组指定索引的值推送至栈顶  |
|  0x30  |  faload  |  将float型数组指定索引的值推送至栈顶  |
|  0x31  |  daload  |  将double型数组指定索引的值推送至栈顶  |
|  0x32  |  aaload  |  将引用型数组指定索引的值推送至栈顶  |
|  0x33  |  baload  |  将boolean或byte型数组指定索引的值推送至栈顶  |
|  0x34  |  caload  |  将char型数组指定索引的值推送至栈顶  |
|  0x35  |  saload  |  将short型数组指定索引的值推送至栈顶  |
|  0x36  |  istore  |  将栈顶int型数值存入指定本地变量  |
|  0x37  |  lstore  |  将栈顶long型数值存入指定本地变量  |
|  0x38  |  fstore  |  将栈顶float型数值存入指定本地变量  |
|  0x39  |  dstore  |  将栈顶double型数值存入指定本地变量  |
|  0x3a  |  astore  |  将栈顶引用型数值存入指定本地变量  |
|  0x3b  |  istore_0  |  将栈顶int型数值存入第一个本地变量  |
|  0x3c  |  istore_1  |  将栈顶int型数值存入第二个本地变量  |
|  0x3d  |  istore_2  |  将栈顶int型数值存入第三个本地变量  |
|  0x3e  |  istore_3  |  将栈顶int型数值存入第四个本地变量  |
|  0x3f  |  lstore_0  |  将栈顶long型数值存入第一个本地变量  |
|  0x40  |  lstore_1  |  将栈顶long型数值存入第二个本地变量  |
|  0x41  |  lstore_2  |  将栈顶long型数值存入第三个本地变量  |
|  0x42  |  lstore_3  |  将栈顶long型数值存入第四个本地变量  |
|  0x43  |  fstore_0  |  将栈顶float型数值存入第一个本地变量  |
|  0x44  |  fstore_1  |  将栈顶float型数值存入第二个本地变量  |
|  0x45  |  fstore_2  |  将栈顶float型数值存入第三个本地变量  |
|  0x46  |  fstore_3  |  将栈顶float型数值存入第四个本地变量  |
|  0x47  |  dstore_0  |  将栈顶double型数值存入第一个本地变量  |
|  0x48  |  dstore_1  |  将栈顶double型数值存入第二个本地变量  |
|  0x49  |  dstore_2  |  将栈顶double型数值存入第三个本地变量  |
|  0x4a  |  dstore_3  |  将栈顶double型数值存入第四个本地变量  |
|  0x4b  |  astore_0  |  将栈顶引用型数值存入第一个本地变量  |
|  0x4c  |  astore_1  |  将栈顶引用型数值存入第二个本地变量  |
|  0x4d  |  astore_2  |  将栈顶引用型数值存入第三个本地变量  |
|  0x4e  |  astore_3  |  将栈顶引用型数值存入第四个本地变量  |
|  0x4f  |  iastore  |  将栈顶int型数值存入指定数组的指定索引位置  |
|  0x50  |  lastore  |  将栈顶long型数值存入指定数组的指定索引位置  |
|  0x51  |  fastore  |  将栈顶float型数值存入指定数组的指定索引位置  |
|  0x52  |  dastore  |  将栈顶double型数值存入指定数组的指定索引位置  |
|  0x53  |  aastore  |  将栈顶引用型数值存入指定数组的指定索引位置  |
|  0x54  |  bastore  |  将栈顶boolean或byte型数值存入指定数组的指定索引位置  |
|  0x55  |  castore  |  将栈顶char型数值存入指定数组的指定索引位置  |
|  0x56  |  sastore  |  将栈顶short型数值存入指定数组的指定索引位置  |
|  0x57  |  pop  |  将栈顶数值弹出  |
|  0x58  |  pop2  |  将栈顶的一个（long或double类型的)或两个数值弹出（其它）  |
|  0x59  |  dup  |  复制栈顶数值并将复制值压入栈顶  |
|  0x5a  |  dup_x1  |  复制栈顶数值并将两个复制值压入栈顶  |
|  0x5b  |  dup_x2  |  复制栈顶数值并将三个（或两个）复制值压入栈顶  |
|  0x5c  |  dup2  |  复制栈顶一个（long或double类型的)或两个（其它）数值并将复制值压入栈顶  |
|  0x5d  |  dup2_x1  |  复制栈顶的一个或两个值，将其插入栈顶那两个或三个值的下面  |
|  0x5e  |  dup2_x2  |  复制栈顶的一个或两个值，将其插入栈顶那两个、三个或四个值的下面  |
|  0x5f  |  swap  |  将栈最顶端的两个数值互换(数值不能是long或double类型的)  |
|  0x60  |  iadd  |  将栈顶两int型数值相加并将结果压入栈顶  |
|  0x61  |  ladd  |  将栈顶两long型数值相加并将结果压入栈顶  |
|  0x62  |  fadd  |  将栈顶两float型数值相加并将结果压入栈顶  |
|  0x63  |  dadd  |  将栈顶两double型数值相加并将结果压入栈顶  |
|  0x64  |  isub  |  将栈顶两int型数值相减并将结果压入栈顶  |
|  0x65  |  lsub  |  将栈顶两long型数值相减并将结果压入栈顶  |
|  0x66  |  fsub  |  将栈顶两float型数值相减并将结果压入栈顶  |
|  0x67  |  dsub  |  将栈顶两double型数值相减并将结果压入栈顶  |
|  0x68  |  imul  |  将栈顶两int型数值相乘并将结果压入栈顶  |
|  0x69  |  lmul  |  将栈顶两long型数值相乘并将结果压入栈顶  |
|  0x6a  |  fmul  |  将栈顶两float型数值相乘并将结果压入栈顶  |
|  0x6b  |  dmul  |  将栈顶两double型数值相乘并将结果压入栈顶  |
|  0x6c  |  idiv  |  将栈顶两int型数值相除并将结果压入栈顶  |
|  0x6d  |  ldiv  |  将栈顶两long型数值相除并将结果压入栈顶  |
|  0x6e  |  fdiv  |  将栈顶两float型数值相除并将结果压入栈顶  |
|  0x6f  |  ddiv  |  将栈顶两double型数值相除并将结果压入栈顶  |
|  0x70  |  irem  |  将栈顶两int型数值作取模运算并将结果压入栈顶  |
|  0x71  |  lrem  |  将栈顶两long型数值作取模运算并将结果压入栈顶  |
|  0x72  |  frem  |  将栈顶两float型数值作取模运算并将结果压入栈顶  |
|  0x73  |  drem  |  将栈顶两double型数值作取模运算并将结果压入栈顶  |
|  0x74  |  ineg  |  将栈顶int型数值取负并将结果压入栈顶  |
|  0x75  |  lneg  |  将栈顶long型数值取负并将结果压入栈顶  |
|  0x76  |  fneg  |  将栈顶float型数值取负并将结果压入栈顶  |
|  0x77  |  dneg  |  将栈顶double型数值取负并将结果压入栈顶  |
|  0x78  |  ishl  |  将int型数值左移位指定位数并将结果压入栈顶  |
|  0x79  |  lshl  |  将long型数值左移位指定位数并将结果压入栈顶  |
|  0x7a  |  ishr  |  将int型数值右（符号）移位指定位数并将结果压入栈顶  |
|  0x7b  |  lshr  |  将long型数值右（符号）移位指定位数并将结果压入栈顶  |
|  0x7c  |  iushr  |  将int型数值右（无符号）移位指定位数并将结果压入栈顶  |
|  0x7d  |  lushr  |  将long型数值右（无符号）移位指定位数并将结果压入栈顶  |
|  0x7e  |  iand  |  将栈顶两int型数值作“按位与”并将结果压入栈顶  |
|  0x7f  |  land  |  将栈顶两long型数值作“按位与”并将结果压入栈顶  |
|  0x80  |  ior  |  将栈顶两int型数值作“按位或”并将结果压入栈顶  |
|  0x81  |  lor  |  将栈顶两long型数值作“按位或”并将结果压入栈顶  |
|  0x82  |  ixor  |  将栈顶两int型数值作“按位异或”并将结果压入栈顶  |
|  0x83  |  lxor  |  将栈顶两long型数值作“按位异或”并将结果压入栈顶  |
|  0x84  |  iinc  |  将指定int型变量增加指定值（i++,  |
|  0x85  |  i2l  |  将栈顶int型数值强制转换成long型数值并将结果压入栈顶  |
|  0x86  |  i2f  |  将栈顶int型数值强制转换成float型数值并将结果压入栈顶  |
|  0x87  |  i2d  |  将栈顶int型数值强制转换成double型数值并将结果压入栈顶  |
|  0x88  |  l2i  |  将栈顶long型数值强制转换成int型数值并将结果压入栈顶  |
|  0x89  |  l2f  |  将栈顶long型数值强制转换成float型数值并将结果压入栈顶  |
|  0x8a  |  l2d  |  将栈顶long型数值强制转换成double型数值并将结果压入栈顶  |
|  0x8b  |  f2i  |  将栈顶float型数值强制转换成int型数值并将结果压入栈顶  |
|  0x8c  |  f2l  |  将栈顶float型数值强制转换成long型数值并将结果压入栈顶  |
|  0x8d  |  f2d  |  将栈顶float型数值强制转换成double型数值并将结果压入栈顶  |
|  0x8e  |  d2i  |  将栈顶double型数值强制转换成int型数值并将结果压入栈顶  |
|  0x8f  |  d2l  |  将栈顶double型数值强制转换成long型数值并将结果压入栈顶  |
|  0x90  |  d2f  |  将栈顶double型数值强制转换成float型数值并将结果压入栈顶  |
|  0x91  |  i2b  |  将栈顶int型数值强制转换成byte型数值并将结果压入栈顶  |
|  0x92  |  i2c  |  将栈顶int型数值强制转换成char型数值并将结果压入栈顶  |
|  0x93  |  i2s  |  将栈顶int型数值强制转换成short型数值并将结果压入栈顶  |
|  0x94  |  lcmp  |  比较栈顶两long型数值大小，并将结果（1，0，-1）压入栈顶  |
|  0x95  |  fcmpl  |  比较栈顶两float型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为NaN时，将-1压入栈顶  |
|  0x96  |  fcmpg  |  比较栈顶两float型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为NaN时，将1压入栈顶  |
|  0x97  |  dcmpl  |  比较栈顶两double型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为NaN时，将-1压入栈顶  |
|  0x98  |  dcmpg  |  比较栈顶两double型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为NaN时，将1压入栈顶  |
|  0x99  |  ifeq  |  当栈顶int型数值等于0时跳转  |
|  0x9a  |  ifne  |  当栈顶int型数值不等于0时跳转  |
|  0x9b  |  iflt  |  当栈顶int型数值小于0时跳转  |
|  0x9c  |  ifge  |  当栈顶int型数值大于等于0时跳转  |
|  0x9d  |  ifgt  |  当栈顶int型数值大于0时跳转  |
|  0x9e  |  ifle  |  当栈顶int型数值小于等于0时跳转  |
|  0x9f  |  if_icmpeq  |  比较栈顶两int型数值大小，当结果等于0时跳转  |
|  0xa0  |  if_icmpne  |  比较栈顶两int型数值大小，当结果不等于0时跳转  |
|  0xa1  |  if_icmplt  |  比较栈顶两int型数值大小，当结果小于0时跳转  |
|  0xa2  |  if_icmpge  |  比较栈顶两int型数值大小，当结果大于等于0时跳转  |
|  0xa3  |  if_icmpgt  |  比较栈顶两int型数值大小，当结果大于0时跳转  |
|  0xa4  |  if_icmple  |  比较栈顶两int型数值大小，当结果小于等于0时跳转  |
|  0xa5  |  if_acmpeq  |  比较栈顶两引用型数值，当结果相等时跳转  |
|  0xa6  |  if_acmpne  |  比较栈顶两引用型数值，当结果不相等时跳转  |
|  0xa7  |  goto  |  无条件跳转  |
|  0xa8  |  jsr  |  跳转至指定16位offset位置，并将jsr下一条指令地址压入栈顶  |
|  0xa9  |  ret  |  返回至本地变量指定的index的指令位置（一般与jsr,  |
|  0xaa  |  tableswitch  |  用于switch条件跳转，case值连续（可变长度指令）  |
|  0xab  |  lookupswitch  |  用于switch条件跳转，case值不连续（可变长度指令）  |
|  0xac  |  ireturn  |  从当前方法返回int  |
|  0xad  |  lreturn  |  从当前方法返回long  |
|  0xae  |  freturn  |  从当前方法返回float  |
|  0xaf  |  dreturn  |  从当前方法返回double  |
|  0xb0  |  areturn  |  从当前方法返回对象引用  |
|  0xb1  |  return  |  从当前方法返回void  |
|  0xb2  |  getstatic  |  获取指定类的静态域，并将其值压入栈顶  |
|  0xb3  |  putstatic  |  为指定的类的静态域赋值  |
|  0xb4  |  getfield  |  获取指定类的实例域，并将其值压入栈顶  |
|  0xb5  |  putfield  |  为指定的类的实例域赋值  |
|  0xb6  |  invokevirtual  |  调用实例方法  |
|  0xb7  |  invokespecial  |  调用超类构造方法，实例初始化方法，私有方法  |
|  0xb8  |  invokestatic  |  调用静态方法  |
|  0xb9  |  invokeinterface  |  调用接口方法  |
|  0xba  |  invokedynamic  |  调用动态链接方法  |
|  0xbb  |  new  |  创建一个对象，并将其引用值压入栈顶  |
|  0xbc  |  newarray  |  创建一个指定原始类型（如int,  |
|  0xbd  |  anewarray  |  创建一个引用型（如类，接口，数组）的数组，并将其引用值压入栈顶  |
|  0xbe  |  arraylength  |  获得数组的长度值并压入栈顶  |
|  0xbf  |  athrow  |  将栈顶的异常抛出  |
|  0xc0  |  checkcast  |  检验类型转换，检验未通过将抛出ClassCastException  |
|  0xc1  |  instanceof  |  检验对象是否是指定的类的实例，如果是将1压入栈顶，否则将0压入栈顶  |
|  0xc2  |  monitorenter  |  获得对象的锁，用于同步方法或同步块  |
|  0xc3  |  monitorexit  |  释放对象的锁，用于同步方法或同步块  |
|  0xc4  |  wide  |  扩大本地变量索引的宽度  |
|  0xc5  |  multianewarray  |  创建指定类型和指定维度的多维数组（执行该指令时，操作栈中必须包含各维度的长度值），并将其引用值压入栈顶  |
|  0xc6  |  ifnull  |  为null时跳转  |
|  0xc7  |  ifnonnull  |  不为null时跳转  |
|  0xc8  |  goto_w  |  无条件跳转  |
|  0xc9  |  jsr_w  |  跳转至指定32位offset位置，并将jsr_w下一条指令地址压入栈顶  |
|        |    | 最后三个为保留指令 |
|  0xca  |  breakpoint  |  调试时的断点标记  |
|  0xfe  |  impdep1  |  为特定软件而预留的语言后门  |
|  0xff  |  impdep2  |  为特定硬件而预留的语言后门  |
|    |    |    |



