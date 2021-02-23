[TOC]

# 分布式文件系统

## GlusterFS

GlusterFS 是由美国的 Gluster 公司开发的 POSIX 分布式文件系统（以 GPL 开源），2007 年发布第一个公开版本，2011 年被 Redhat 收购。

它的基本思路就是通过一个无状态的中间件把多个单机文件系统融合成统一的名字空间（namespace）提供给用户。这个中间件是由一系列可叠加的转换器（Translator）实现，每个转换器解决一个问题，比如数据分布、复制、拆分、缓存、锁等等，用户可以根据具体的应用场景需要灵活配置。

## GFS

Google 的 GFS 是分布式文件系统中的先驱和典型代表，由早期的 BigFiles 发展而来。在 2003 年发表的论文中详细阐述了它的设计理念和细节，对业界影响非常大，后来很多分布式文件系统都是参照它的设计。

**顾名思义，BigFiles/GFS 是为大文件优化设计的，并不适合平均文件大小在 1MB 以内的场景。** GFS 的架构入下图所示。

![img](/Users/dongzhonghua03/Documents/github/dongzhonghua.github.io/pic/GoogleFileSystemGFS.png)

GFS 有一个 Master 节点来管理元数据（全部加载到内存，快照和更新日志写到磁盘），文件划分成 64MB 的 Chunk 存储到几个 ChunkServer 上（直接使用单机文件系统）。文件只能追加写，不用担心 Chunk 的版本和一致性问题（可以用长度当做版本）。

这个使用完全不同的技术来解决元数据和数据的设计使得系统的复杂度大大简化，也有足够的扩展能力（如果平均文件大小大于 256MB，Master 节点每 GB 内存可以支撑约 1PB 的数据量）。放弃支持 POSIX 文件系统的部分功能（比如随机写、扩展属性、硬链接等）也进一步简化了系统复杂度，以换取更好的系统性能、鲁棒性和可扩展性。

因为 GFS 的成熟稳定，使得 Google 可以更容易地构建上层应用（MapReduce、BigTable 等）。后来，Google 开发了拥有更强可扩展能力的下一代存储系统 Colossus，把元数据和数据存储彻底分离，实现了元数据的分布式（自动 Sharding），以及使用 Reed Solomon 编码来降低存储空间占用从而降低成本。

## HDFS

出自 Yahoo 的 Hadoop 算是 Google 的 GFS、MapReduce 等的开源 Java 实现版，HDFS 也是基本照搬 GFS 的设计，这里就不再重复了，下图是 HDFS 的架构图：

![img](/Users/dongzhonghua03/Documents/github/dongzhonghua.github.io/pic/HDFS.png)



HDFS 的可靠性和可扩展能力还是非常不错的，有不少几千节点和 100PB 级别的部署，支撑大数据应用表现还是很不错的，少有听说丢数据的案例（因为没有配置回收站导致数据被误删的除外）。

**HDFS 的 HA 方案是后来补上的，做得比较复杂，以至于最早做这个 HA 方案的 Facebook 在很长一段时间（至少 3 年）内都是手动做故障切换（不信任自动故障切换）。**

因为 NameNode 是 Java 实现的，依赖于预先分配的堆内存大小，分配不足容易触发 Full GC 而影响整个系统的性能。有一些团队尝试把它用 C++ 重写了，但还没看到有成熟的开源方案。

HDFS 也缺乏成熟的非 Java 客户端，使得大数据（Hadoop 等工具）以外的场景（比如深度学习等）使用起来不太方便。