import { Card } from '@/components/ui/card';
import { MapPin, Heart, Users, Book } from 'lucide-react';

const About = () => {
  const features = [
    {
      icon: <Heart className="w-8 h-8 text-warm-gold" />,
      title: "Loving Community",
      description: "A welcoming family where everyone belongs and grows together in faith."
    },
    {
      icon: <Book className="w-8 h-8 text-warm-gold" />,
      title: "Biblical Teaching",
      description: "Grounded in Scripture with practical application for daily living and spiritual growth."
    },
    {
      icon: <Users className="w-8 h-8 text-warm-gold" />,
      title: "Active Ministry",
      description: "Engaging ministries for all ages, especially our vibrant youth community."
    }
  ];

  return (
    <section id="about" className="py-20 bg-soft-gray">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-spiritual mb-4">
            About Our Church
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Laver Transformation Ministries is a vibrant community of believers dedicated to 
            spiritual transformation and serving our community in Wamala.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h3 className="text-2xl font-bold text-spiritual mb-6">Our Mission</h3>
            <p className="text-muted-foreground leading-relaxed mb-6">
              We are committed to transforming lives through the power of God's Word and love. 
              Our church serves as a beacon of hope and transformation in the Wamala community, 
              where people from all walks of life come together to worship, learn, and grow.
            </p>
            <div className="flex items-center text-spiritual font-medium">
              <MapPin className="w-5 h-5 mr-2 text-warm-gold" />
              <span>Wamala, along Wamala Katoke Road</span>
            </div>
          </div>

          <div className="grid gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="p-6 hover:shadow-gentle transition-all duration-300 hover:scale-105">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    {feature.icon}
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-spiritual mb-2">
                      {feature.title}
                    </h4>
                    <p className="text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;