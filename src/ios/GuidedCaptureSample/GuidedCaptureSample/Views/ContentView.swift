/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The top-level app view.
*/

import SwiftUI
import os
import RealityKit

private let logger = Logger(subsystem: GuidedCaptureSampleApp.subsystem, category: "ContentView")

/// The root of the SwiftUI View graph.
struct ContentView: View {
    @Environment(AppDataModel.self) var appModel
    
    var body: some View {
        ZStack {
            // Show camera view or feedback based on state
            if appModel.state == .autoCapturing,
               let session = appModel.objectCaptureSession {
                // Show camera view during auto capture
                ObjectCaptureView(session: session)
                    .overlay(
                        VStack {
                            Text("Auto Capturing - Orbit \(appModel.orbit.rawValue + 1)")
                                .foregroundColor(.white)
                                .padding()
                                .background(Color.black.opacity(0.7))
                                .cornerRadius(10)
                            
                            if appModel.robotState == .disconnected {
                                Text("No Robot Connected - Testing Mode")
                                    .foregroundColor(.yellow)
                                    .padding()
                                    .background(Color.black.opacity(0.7))
                                    .cornerRadius(10)
                            }
                        }
                    )
                    .ignoresSafeArea()
            } else {
                PrimaryView()
            }
            
            // Auto capture toggle button
            VStack {
                Spacer()
                HStack {
                    Spacer()
                    Button(action: {
                        Task { @MainActor in
                            appModel.toggleAutoMode()
                        }
                    }) {
                        Text(appModel.state == .autoCapturing ? "Stop Auto Capture" : "Start Auto Capture")
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    .padding()
                }
            }
        }
        .onAppear {
            UIApplication.shared.isIdleTimerDisabled = true
        }
        .onDisappear {
            UIApplication.shared.isIdleTimerDisabled = false
        }
    }
}
