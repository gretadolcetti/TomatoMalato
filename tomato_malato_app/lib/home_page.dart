import 'package:flutter/material.dart';
import 'my_webview.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Home Page"),
      ),
      body: Center(
        child: ElevatedButton(
          child: Text("Open Webpage"),
          onPressed: () {
            Navigator.of(context).push(MaterialPageRoute(
                builder: (BuildContext context) => MyWebView(
                  title: "DigitalOcean",
                  selectedUrl: "http://10.0.2.2:5000",
                )
            ));
          },
        ),
      ),
    );
  }
}