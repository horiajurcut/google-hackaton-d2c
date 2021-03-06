//
//  HBTimelineItem.m
//  HummingBox
//
//  Created by Stefan Filip on 23/11/13.
//  Copyright (c) 2013 Hack Attack. All rights reserved.
//

#import "HBTimelineItem.h"

@implementation HBTimelineItem

- (id)initWithAttributes:(NSDictionary *)attributes {
    self = [super initWithAttributes:attributes];
    if (self) {
        _startedDate = [NSDate dateWithTimeIntervalSince1970:[[attributes valueForKey:@"startedDate"] doubleValue]];
        _isPlaying = [[attributes valueForKey:@"status"] integerValue] == 1;
    }
    return self;
}

@end
