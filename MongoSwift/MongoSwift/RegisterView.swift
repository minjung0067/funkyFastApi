//
//  RegisterView.swift
//  MongoSwift
//
//  Created by Minjung Lee on 6/24/24.
//

import SwiftUI

struct RegisterView: View {
    @State private var username = ""
    @State private var email = ""
    @State private var password = ""
    @State private var message = ""
    
    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            TextField("Email", text: $email)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            SecureField("Password", text: $password)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            Button(action: register) {
                Text("Register")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
            .padding()
            
            Text(message)
                .padding()
                .foregroundColor(.red)
        }
        .padding()
    }
    
    func register() {
        guard let url = URL(string: "http://localhost:8000/user/signup") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let user = ["username": username, "email": email, "password": password]
        guard let httpBody = try? JSONSerialization.data(withJSONObject: user, options: []) else { return }
        request.httpBody = httpBody
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    message = "Network error: \(error.localizedDescription)"
                }
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
                DispatchQueue.main.async {
                    message = "Server error"
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    message = "No data received"
                }
                return
            }
            
            do {
                let decoder = JSONDecoder()
                let response = try decoder.decode([String: String].self, from: data)
                DispatchQueue.main.async {
                    message = response["message"] ?? "Unknown error"
                }
            } catch {
                DispatchQueue.main.async {
                    message = "Decoding error: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}

struct RegisterView_Previews: PreviewProvider {
    static var previews: some View {
        RegisterView()
    }
}
