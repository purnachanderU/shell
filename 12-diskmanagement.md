One of the common tasks in Linux system administration and DevOps is managing disk storage. Adding a new disk is not just about attaching the disk to a server — we also need to partition it, create a filesystem, mount it, and make sure it remains available after a reboot.

For example, when a new 25 GB disk is attached to a Linux server, I first use `lsblk` to identify the new disk.

Once the disk is identified, I create a GPT partition table and partition using `parted`.

`sudo parted /dev/nvme1n1 --script mklabel gpt mkpart primary 0% 100%`

After creating the partition, I format it with the required filesystem. In this example, I'm using XFS.

`sudo mkfs.xfs -f /dev/nvme1n1p1`

Next, I create a mount point and mount the filesystem.

`sudo mkdir -p /data`

`sudo mount /dev/nvme1n1p1 /data`

I then verify that the filesystem is mounted correctly using `df -hT`.

The important part is making the mount persistent. If we only use the `mount` command, the filesystem will not automatically be mounted after a server reboot.

So I get the filesystem UUID using `blkid` and add the UUID to `/etc/fstab`.

`UUID=d68b606a-4df3-44c2-bd74-418fa36e9fa2 /data xfs defaults,nofail 0 2`

Using UUID is preferable to depending on a device name such as `/dev/nvme1n1p1`, because device names can change depending on how disks are detected.

Before considering the configuration complete, I validate `/etc/fstab` using:

`sudo mount -a`

If there are no errors, I verify the mount again with `df -hT`.

Another common requirement in production environments is expanding existing storage. For an LVM-based filesystem, the process can involve extending the underlying partition with `growpart` and then extending the logical volume using `lvextend`.

For example:

`sudo growpart /dev/nvme0n1 4`

`sudo lvextend -L +10G /dev/RootVG/rootVol`

`sudo lvextend -L +10G /dev/RootVG/varVol`

One important point is that extending the logical volume and growing the filesystem are separate operations. Depending on the filesystem, we may also need `xfs_growfs` for XFS or `resize2fs` for ext4.

A few Linux commands I frequently use for storage and system troubleshooting are:

`lsblk` — view disks, partitions, and their relationships.

`df -hT` — check mounted filesystems, disk usage, and filesystem types.

`du -sh *` — identify how much space files and directories are consuming.

`free -m` — check memory usage.

Understanding these commands and the underlying concepts is important for troubleshooting disk-full issues, adding storage, expanding filesystems, and maintaining Linux servers in production environments.

Linux storage management is one of those areas where knowing the commands is useful, but understanding what happens at the disk, partition, filesystem, and LVM levels is even more important.

