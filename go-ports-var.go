package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

type GHTags []struct {
	Name       string `json:"name"`
	ZipballURL string `json:"zipball_url"`
	TarballURL string `json:"tarball_url"`
	Commit     struct {
		Sha string `json:"sha"`
		URL string `json:"url"`
	} `json:"commit"`
	NodeID string `json:"node_id"`
}

func usage() {
	fmt.Println("Usage:", os.Args[0], "github.com/org/project")
	os.Exit(0)
}

func parseGHString(ghUrl string) (string, string, string, error) {
	if len(strings.Split(ghUrl, "/")) != 3 {
		return "", "", "", fmt.Errorf("%s isn't in the form of github.com/org/project\n", ghUrl)
	}
	splittedUrl := strings.Split(ghUrl, "/")
	gh, org, project := splittedUrl[0], splittedUrl[1], splittedUrl[2]
	return gh, org, project, nil
}

func getGHTags(c http.Client, gh, org, project string) (*GHTags, error) {
	path := fmt.Sprintf("https://api.%s/repos/%s/%s/tags", gh, org, project)
	req, err := http.NewRequest("GET", path, nil)
	if err != nil {
		return &GHTags{}, err
	}
	resp, err := c.Do(req)
	if err != nil {
		return &GHTags{}, err
	}
	expected := 200
	if resp.StatusCode != expected {
		return &GHTags{}, fmt.Errorf("I didn't get a %d from Github, got a %d\n",
			expected, resp.StatusCode)
	}
	defer resp.Body.Close()
	data := &GHTags{}
	json.NewDecoder(resp.Body).Decode(data)
	return data, nil
}

func getConfirmationUser(prompt string) (bool, error) {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(prompt)
	input, err := reader.ReadString('\n')
	if err != nil {
		return false, err
	}
	input = strings.Trim(input, "\n")
	return strings.ToLower(input) == "y", nil
}

func getGoReleaseName(c http.Client, gh, org, project, commit string) (string, error) {
	path := fmt.Sprintf("https://proxy.golang.org/%s/%s/%s/@v/v0.0.0-20210101000000-%s.info",
		gh, org, project, commit)
	req, err := http.NewRequest("GET", path, nil)
	if err != nil {
		return "", err
	}
	resp, err := c.Do(req)
	if err != nil {
		return "", err
	}
	// don't ask
	expected := 410
	if resp.StatusCode != expected {
		return "", fmt.Errorf("I didn't get a %d from proxy.golang.org, got a %d\n",
			expected, resp.StatusCode)
	}
	defer resp.Body.Close()
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	body := string(b)
	return strings.TrimSuffix(strings.Split(body, " ")[len(strings.Split(body, " "))-1], ")"), nil
}

func firstLetters(s string, n int) string {
    i := 0
    for j := range s {
        if i == n {
            return s[:j]
        }
        i++
    }
    return s
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Missing argument")
		usage()
	}
	ghUrl := os.Args[1]
	if !strings.HasPrefix(ghUrl, "github.com") {
		fmt.Println(ghUrl)
		fmt.Println("Unsupported forge, only github.com is supported")
		usage()
	}
	gh, org, project, err := parseGHString(ghUrl)
	if err != nil {
		log.Fatal(err)
	}

	c := http.Client{}
	c.Timeout = 10 * time.Second
	tags, err := getGHTags(c, gh, org, project)
	if err != nil {
		log.Fatal(err)
	}
	var commit string
	for _, t := range *tags {
		fmt.Println(t.Name, t.Commit.Sha)
		commit = t.Commit.Sha
		choice, err := getConfirmationUser("Take this commit/tag? (y/N) ")
		if err != nil {
			log.Fatal(err)
		}
		if choice {
			break
		}
	}
	commitShort := firstLetters(commit, 12)
	releaseName, err := getGoReleaseName(c, gh, org, project, commitShort)
	if err != nil {
		log.Fatal(err)
	}
	t, err := time.Parse("20060102150405", releaseName)
	if err != nil {
		log.Fatal(err)
	}
	// time.RFC3339 is 15:04:05
	fmt.Printf("V =\t\t%s\nCID =\t\t%s\n", t.Format("2006-01-02T15-04-05Z07:00"), commit)
	fmt.Printf("\nportgen go %s@v0.0.0-%s-%s\n", ghUrl, releaseName, commitShort)
}
