//
//  HBApiClient.h
//  HummingBox
//
//  Created by Stefan Filip on 23/11/13.
//  Copyright (c) 2013 Hack Attack. All rights reserved.
//

#import "AFHTTPClient.h"
#import "HBUser.h"
#import "HBSong.h"
#import "HBTimelineItem.h"

typedef void (^arrayWithErrorBlock) (NSArray *array, NSError *error);
typedef void (^boolWithErrorBlock) (BOOL result, NSError *error);

@interface HBApiClient : AFHTTPClient

+ (HBApiClient *)sharedClient;
+ (void)loginWithGoogeUserId:(NSString *)googleUserID fullname:(NSString *)fullName andCallback:(boolWithErrorBlock)callback;
+ (void)getTimelineWithCallback:(arrayWithErrorBlock)callback;

@end
