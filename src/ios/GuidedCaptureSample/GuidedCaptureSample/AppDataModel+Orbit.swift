/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
Orbit support for the app data model.
*/

import Foundation

extension AppDataModel {
    enum Orbit: Int, CaseIterable, Identifiable, Comparable {
        case orbit1, orbit2, orbit3

        var id: Int {
            rawValue
        }

        var image: String {
            let imagesByIndex = ["1.circle", "2.circle", "3.circle"]
            return imagesByIndex[id]
        }

        var imageSelected: String {
            let imagesByIndex = ["1.circle.fill", "2.circle.fill", "3.circle.fill"]
            return imagesByIndex[id]
        }

        @MainActor
        func next() -> Self {
            guard let currentIndex = Self.allCases.firstIndex(of: self) else {
                fatalError("Can't find self.")
            }
            
            let nextIndex = Self.allCases.index(after: currentIndex)
            
            // Only auto-advance if in auto capturing mode
            if AppDataModel.instance.state == .autoCapturing {
                // Create message dictionary
                let messageDict = [
                    "command": "orbit_complete",
                    "orbit": currentIndex
                ] as [String: Any]
                
                Task { @MainActor in
                    do {
                        // Use JSONSerialization with proper error handling
                        let jsonData = try JSONSerialization.data(withJSONObject: messageDict, options: [])
                        if let jsonString = String(data: jsonData, encoding: .utf8) {
                            await AppDataModel.instance.sendRobotMessage(jsonString)
                        }
                    } catch {
                        print("Error creating JSON message: \(error)")
                    }
                }
            }
            
            return Self.allCases[nextIndex == Self.allCases.endIndex ? Self.allCases.endIndex - 1 : nextIndex]
        }

        static func < (lhs: AppDataModel.Orbit, rhs: AppDataModel.Orbit) -> Bool {
            guard let lhsIndex = Self.allCases.firstIndex(of: lhs),
                  let rhsIndex = Self.allCases.firstIndex(of: rhs) else {
                return false
            }
            return lhsIndex < rhsIndex
        }
    }
}
