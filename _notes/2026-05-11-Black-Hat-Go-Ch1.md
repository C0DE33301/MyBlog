---
layout: post
title: Black Hat Go
---

# Index
- [Set Up](#set-up)
- [Go tool commands](#go-tool-commands)
    - [`go run`](#go-run)
    - [`go build`](#go-build)
    - [Cross-compiling](#cross-compiling)
        - [The command line](#the-command-line)
        - [Code comments](#code-comments)
        - [File suffix naming convention](#file-suffix-naming-convention)
    - [`go doc`](#go-doc)
    - [`go get`](#go-get)
    - [`go fmt`](#go-fmt)
    - [`golint`](#golint)
    - [`go vet`](#go-vet)
    - [`go test`](#go-test)
    - [`go cover`](#go-cover)
    - [`go imports`](#go-imports)
    - [Go Playground](#go-playground)
- [Go basics](#go-basics)
    - [Primitive Data Types](#primitive-data-types)
    - [Slices](#slices)
    - [Maps](#maps)
    - [Pointers](#pointers)
    - [Structs](#structs)
    - [Interface](#interface)
    - [`if`/`else`](#ifelse)
    - [Switch](#switch)
    - [Type switch](#type-switch)
    - [For loops](#for-loops)
    - [Goroutines](#goroutines)
    - [Error Handling](#error-handling)
    - [JSON](#json)
    - [XML](#json)

## Set Up
- Install GO, `sudo pacman -S go`
- The Go binary location, `set GOROOT=/path/to/go`
- The Go workspace location, `set GOPATH=$HOME/gocode`
    - Create the main dir for example, `~/gocode`
        - Create three subdir within, `~/gocode/bin`, `~/gocode/pkg`, & `~/gocode/src`.
            - **bin**, Contains compiled and installed Go executable binaries.
            - **pkg**, Stores packages objects, including third-party Go dependencies.
            - **src**, Contains all the source code.
- Pick an IDE, any is fine.

## Go tool commands
### `go run`
Compiles and executes the main package.

>~/gocode/src/testproject/main.go
{:.filename}
{% highlight go linenos %}
package main
import (
    "fmt"
)
func main() {
    fmt.Println("Hello, World!")
}
{% endhighlight %}

Execute the file 
{% highlight go linenos %}
go run main.go
{% endhighlight %}

### `go build`
Compiles with its packages and dependencies. Creates the bianry file without executing the program.

>~/gocode/src/testproject/hello.go
{:.filename}
{% highlight go linenos %}
package main
import (
    "fmt"
)
func main() {
    fmt.Println("Hello, World!")
}
{% endhighlight %}

Compile the file, this will create the file, `hello` executable.
{% highlight go linenos %}
go build hello.go
{% endhighlight %}

### Cross-compiling
#### The command line
{% highlight go linenos %}
GOOS="linux" GOARCH="amd64" go build hello.go
{% endhighlight %}
Linux: `hello: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped`
#### Code comments
#### File suffix naming convention

### `go doc`
Documentation about a package, function, methods, or variable. Taken directly out of the source code comments.

{% highlight go linenos %}
go doc fmt.Println
{% endhighlight %}

output
{% highlight diff linenos %}
package fmt // import "fmt"

func Println(a ...any) (n int, err error)
    Println formats using the default formats for its operands and writes to
    standard output. Spaces are always added between operands and a newline
    is appended. It returns the number of bytes written and any write error
    encountered.
{% endhighlight %}

### `go get`
`Outdated use go install`
To obtain package source code.

{% highlight go linenos %}
package main

import (
    "fmt"
    "net/http"
    "github.com/stacktitan/ldapauth"
)
{% endhighlight %}

To download the package, `$GOPATH/src` dir
{% highlight go linenos %}
go get github.com/stacktitan/ldapauth
{% endhighlight %}

### `go fmt`
Automatically formats source code. Proper line brakes, indentation, and brace alignment.

### `golint`
- To install `golint`, `go get -u golang.org/x/lint/golint` or `go install golang.org/x/lint/golint@latest`
- Reports stlye mistakes, missing comments, variable naming, etc.

### `go vet`
Attempts to identify issues.

### `go test`
To run unit tests and benchmarks.

### `go cover`
To check for test coverage

### `go imports`
To fix import statements, etc.

### Go Playground
- `play.golang.org`
- `go.dev/play`

## Go basics
### Primitive Data Types
`bool`, `strings`, `int`, `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`, `byte`, `rune`, `float32`, `float64`, `complex64`, & `complex128`.
{% highlight go linenos %}
var x = "Hello, World!"
z := int(42)
{% endhighlight %}
### Slices
Like Arrays
{% highlight go linenos %}
var s = make([]string, 0)
s = append(s, "some string")
{% endhighlight %}
- `append()`, To add a new item to a slice.

### Maps
Arrays, unordered lists of key/value pairs.
{% highlight go linenos %}
var m = make(map[string]string)
m["some value"] = "some value"
{% endhighlight %}
- `make()`, Initialize each variable.
- `m["some value"]`, `some`:`key` & `value`:value

### Pointers
Points to a particular are in memory & retrieve the value.
{% highlight go linenos %}
var count = int(42)
ptr := &count
fmt.Println(*ptr)
*ptr = 100
fmt.Println(count)
{% endhighlight %}
- `&`, Operator to retrieve the value. Creates a pointer.
- `*`, Operator to dereference the address.
- `*ptr = 100`, To assign a new value to the memory location pointed to `ptr`.

### Structs
To define new data types by specifying the type's associated fields and methods.
{% highlight go linenos %}
type Person struct {
	Name string
	Age  int
}
func (p *Person) SayHello() {
	fmt.Println("Hello,", p.Name, ". You're old!", p.Age)
}
func main() {
	var guy = new(Person)
	guy.Name = "Dave"
	guy.Age = 42
	guy.SayHello()
}
{% endhighlight %}

### Interface
A blueprint or a contract. A set of actions.
{% highlight go linenos %}
type Person struct {
	Name string
	Age  int
}

type Friend interface {
	SayHello()
}

func (p *Person) SayHello() {
	fmt.Println("Hello,", p.Name, ". You're old!", p.Age)
}

func Greet(f Friend) {
	f.SayHello()
}

func main() {
	var guy = new(Person)
	guy.Name = "Dave"
	guy.Age = 42
	Greet(guy)
}
{% endhighlight %}

### `if`/`else`
{% highlight go linenos %}
if x == 1 {
    fmt.Println("X is equal to 1")
} else {
    fmt.Println("X is not equal to 1")
}
{% endhighlight %}

### Switch
{% highlight go linenos %}
switch x {
    case "foo":
        fmt.Println("Found foo")
    case "bar":
        fmt.Println("Found bar")
    default:
        fmt.Println("Default case")
}
{% endhighlight %}

### Type switch
{% highlight go linenos %}
func foo(i interface{}) {
    switch v := i.(type) {
        case int:
            fmt.Println("I'm an integer")
        case string:
            fmt.Println("I'm a string")
        default:
            fmt.Println("Unknown type!")
    }
}
{% endhighlight %}

### For loops
{% highlight go linenos %}
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
{% endhighlight %}

Loops over a collection, a slice/nmap.
{% highlight go linenos %}
nums := []int{2, 4, 6, 8}
for idx, val := range nums {
    fmt.Println(idx, val)
}
{% endhighlight %}
- `nums := []int{2, 4, 6, 8}`, A slice of integers.

### Goroutines
{% highlight go linenos %}
func f() {
    fmt.Println("f function")
}

func main() {
    go f()
    time.Sleep(1 * time.Second)
    fmt.Println("main function")
}
{% endhighlight %}

### Channels
{% highlight go linenos %}
func strlen(s string, c chan int) {
    c <- len(s)
}

func main() {
    c := make(chan int)
    go strlen("Salutations", c)
    go strlen("World", c)
    x, y := <-c, <-c
    fmt.Println(x, y, x+y)
}
{% endhighlight %}
- `<-`, The data is flowing to or from a channel.

### Error Handling
Returns a string value, as an error.

Interface
{% highlight go linenos %}
type error interface {
    Error() string
}
{% endhighlight %}
String
{% highlight go linenos %}
type MyError string
func (e MyError) Error() string {
    return string(e)
}
{% endhighlight %}
{% highlight go linenos %}
func foo() error {
    return errors.New("Some Error Occurred")
}

func main() {
    if err := foo(); err != nil {
        //Handle the error
    }
}
{% endhighlight %}
- `nil`, The function ran without error.
- **non-nil**, The function ran with error.

### JSON
- `encoding/json`
{% highlight go linenos %}
type Foo struct {
    Bar string
    Baz string
}

func main() {
    f := Foo{"Joe Junior", "Hello Shabado"}
    b, _ := json.Marshal(f)
    fmt.Println(string(b))
    json.Unmarshal(b, &f)
}
{% endhighlight %}
- `Marshal()`, Encodes the struct to JSON, returning a byte slice.
- `{"Bar":"Joe Junior", "Baz":"Hello Shabado"}`

### XML
- `encoding/xml`
{% highlight go linenos %}
type Foo struct {
    Bar string `xml:"id,attr"`
    Baz string `xml:"parent>child"`
}

func main() {

}
{% endhighlight %}
- `` ` ``, Field tags
- `"`. Directive